import 'dart:async';
import 'dart:io';

import 'package:camera/camera.dart';
import 'package:flutter/material.dart';

import 'package:http/http.dart' as http;

import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';
import 'package:flutter/services.dart';
import 'package:path_provider/path_provider.dart';
import 'package:image_picker/image_picker.dart';

import 'muscle_group_selection_page.dart';
import 'exercise_data_page.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  final cameras = await availableCameras();
  final firstCamera = cameras.first;

  SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp])
      .then((value) => runApp(
            MaterialApp(
              debugShowCheckedModeBanner: false,
              theme: ThemeData.dark(),
              home: TakePictureScreen(
                // Pass the appropriate camera to the TakePictureScreen widget.
                camera: firstCamera,
              ),
            ),
          ));
}

// A screen that allows users to take a picture using a given camera.
class TakePictureScreen extends StatefulWidget {
  const TakePictureScreen({
    super.key,
    required this.camera,
  });

  final CameraDescription camera;

  @override
  TakePictureScreenState createState() => TakePictureScreenState();
}

class TakePictureScreenState extends State<TakePictureScreen> {
  late CameraController _controller;
  late Future<void> _initializeControllerFuture;
  String machineName = '';

  @override
  void initState() {
    super.initState();
    // To display the current output from the Camera,
    // create a CameraController.
    _controller = CameraController(
      // Get a specific camera from the list of available cameras.
      widget.camera,
      // Define the resolution to use.
      ResolutionPreset.medium,
      enableAudio: false,
    );

    // Next, initialize the controller. This returns a Future.
    _initializeControllerFuture = _controller.initialize();
  }

  Future<String> getLabel(File imageFile) async {
    List<int> imageBytes = imageFile.readAsBytesSync();

    var uri = Uri.parse("http://3.88.136.90:5000/label");

    try {
      final http.Response response = await http
          .post(
            uri,
            headers: <String, String>{
              "Content-Type": "application/octet-stream"
            },
            body: imageBytes,
          )
          .timeout(const Duration(seconds: 3));

      if (response.statusCode == 200) {
        return (response.body);
      } else {
        throw Exception("NoServerResponse");
      }
    } on TimeoutException catch (_) {
      rethrow;
    } on SocketException catch (_) {
      rethrow;
    }
  }

  ClipRect getCameraPreview(BuildContext context) {
    final mediaSize = MediaQuery.of(context).size;
    final scale = 1 / (_controller.value.aspectRatio * mediaSize.aspectRatio);
    return ClipRect(
      clipper: _MediaSizeClipper(mediaSize),
      child: Transform.scale(
        scale: scale,
        alignment: Alignment.topCenter,
        child: CameraPreview(_controller),
      ),
    );
  }

  Future<List<Map>> getMachineData(String machineLabel) async {
    Directory documentsDirectory = await getApplicationDocumentsDirectory();
    String path = join(documentsDirectory.path, "SeniorProjectDB.db");
    ByteData data = await rootBundle.load("assets/database/SeniorProjectDB.db");
    List<int> bytes =
        data.buffer.asUint8List(data.offsetInBytes, data.lengthInBytes);
    await File(path).writeAsBytes(bytes);
    Database db = await openDatabase(path);
    final query = """
      SELECT 
        Machine.name as machine, Exercise.name as exercise, 
	      Exercise.Description as exercise_description, 
	      Exercise.VideoURL as video_url, Exercise.TargetMuscle as target_muscle
      FROM Machine, Exercise
      INNER JOIN machineToExercise ON Machine.ID = machineToExercise.machineID  
        AND Exercise.ID = machineToExercise.exerciseID
      WHERE Machine.Name = "$machineLabel"
    """;

    try {
      List<Map> Machine = await db.rawQuery(query);
      return Machine;
    } catch (e) {
      print("Error fetching machines for $machineLabel: $e");
      print('///////////// $db //////////////');
      return [];
    }
  }

  Future<void> _navigateToMucleGroupSelection(
      BuildContext context, List<Map> exercises) async {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (context) => MuscleGroupSelectionPage(exercises),
      ),
    );
  }

  Future<void> _navigateToExerciseData(
      BuildContext context, List<Map> exerciseData) async {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (context) => ExerciseDataPage(exerciseData),
      ),
    );
  }

  Future<File> _getImageFromGallery() async {
    final pickedImage =
        await ImagePicker().pickImage(source: ImageSource.gallery);

    if (pickedImage != null) {
      return File(pickedImage.path);
    }
    throw Exception("No Image Selected");
  }

  Future<T?> displayErrorMessage<T>(
      BuildContext context, String title, String message) {
    print("Function got called");
    return showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: Text(title),
          content: Text(message),
          actions: <Widget>[
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: const Text('OK'),
            ),
          ],
        );
      },
    );
  }

  void processImage(BuildContext context, File image) async {
    try {
      String label = await getLabel(image);

      if (label == 'No Match') {
        const errorTitle = 'CV Error';
        const errorMsg =
            'We could not figure out what machine that is. Try scanning from a different angle.';
        displayErrorMessage(context, errorTitle, errorMsg);
      } else {
        getMachineData(label).then((machineData) {
          if (machineData.isNotEmpty) {
            if (machineData.length == 1) {
              _navigateToExerciseData(context, machineData);
            } else {
              _navigateToMucleGroupSelection(context, machineData);
            }
          } else {
            const errorTitle = 'Database Error.';
            const errorMsg =
                'Looks like we are having issues. Our team will fix them soon!';
            displayErrorMessage(context, errorTitle, errorMsg);
          }
        });
      }
    } catch (_) {
      const errorTitle = 'Server Error.';
      const errorMsg =
          'Looks like we cannot communicate with the server. Make sure you are connected to the internet.';
      displayErrorMessage(context, errorTitle, errorMsg);
    }
  }

  @override
  void dispose() {
    // Dispose of the controller when the widget is disposed.
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: <Widget>[
          // Camera preview
          FutureBuilder<void>(
            future: _initializeControllerFuture,
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.done) {
                return getCameraPreview(context);
              } else {
                return const Center(child: CircularProgressIndicator());
              }
            },
          ),

          Container(
            padding: const EdgeInsets.only(
                top: 40.0, left: 20.0, right: 20.0, bottom: 20.0),
            child: Stack(
              children: [
                //
                // Logo
                Align(
                  alignment: Alignment.topLeft,
                  child: Image.asset(
                    'assets/logo.png',
                    width: 60.0,
                  ),
                ),

                // Gallery picker button
                Align(
                  alignment: Alignment.bottomLeft,
                  child: FloatingActionButton(
                    onPressed: () async {
                      final image = await _getImageFromGallery();
                      processImage(context, image);
                    },
                    child: const Icon(Icons.image),
                  ),
                ),

                // Take picture button
                Align(
                    alignment: Alignment.bottomCenter,
                    child: Container(
                      height: 90.0,
                      width: 90.0,
                      child: FittedBox(
                        child: FloatingActionButton(
                          onPressed: () async {
                            await _initializeControllerFuture;

                            final image =
                                File((await _controller.takePicture()).path);

                            if (!mounted) return;

                            processImage(context, image);
                          },
                          child: const Icon(Icons.camera_alt),
                        ),
                      ),
                    )),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

// A widget that displays the picture taken by the user.
class DisplayPictureScreen extends StatelessWidget {
  final String imagePath;

  const DisplayPictureScreen({super.key, required this.imagePath});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Image.file(File(imagePath)),
    );
  }
}

class _MediaSizeClipper extends CustomClipper<Rect> {
  final Size mediaSize;
  const _MediaSizeClipper(this.mediaSize);
  @override
  Rect getClip(Size size) {
    return Rect.fromLTWH(0, 0, mediaSize.width, mediaSize.height);
  }

  @override
  bool shouldReclip(CustomClipper<Rect> oldClipper) {
    return true;
  }
}
