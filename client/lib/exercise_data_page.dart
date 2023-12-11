import 'package:flutter/material.dart';
import 'package:youtube_player_flutter/youtube_player_flutter.dart';

import 'dot_widget.dart';

class ExerciseDataPage extends StatefulWidget {
  const ExerciseDataPage(this.exerciseData, {super.key});
  final List<Map> exerciseData;

  @override
  ExerciseDataPageState createState() => ExerciseDataPageState();
}

class ExerciseDataPageState extends State<ExerciseDataPage> {
  final _controller = PageController(
    initialPage: 0,
  );

  List<Widget> generatePages() {
    List<Widget> pages = [];
    int index = 0;
    for (var entry in widget.exerciseData) {
      pages.add(Center(
        child: ListView(
          shrinkWrap: true,
          padding: const EdgeInsets.all(0.0),
          children: <Widget>[
            Center(
              child: ListTile(
                title: YoutubePlayer(
                  controller: YoutubePlayerController(
                    initialVideoId:
                        YoutubePlayer.convertUrlToId(entry['video_url'])!,
                    flags: const YoutubePlayerFlags(
                      autoPlay: true,
                      mute: true,
                    ),
                  ),
                  showVideoProgressIndicator: true,
                  progressIndicatorColor: Colors.amber,
                  progressColors: const ProgressBarColors(
                    playedColor: Colors.amber,
                    handleColor: Colors.amberAccent,
                  ),
                ),
              ),
            ),
            Center(
              child: ListTile(
                title: Text('${entry['exercise']}'),
                subtitle: Text('${entry['exercise_description']}'),
                trailing:
                    Image.asset('assets/icons/${entry['target_muscle']}.png'),
              ),
            ),
            Center(
              child: ListTile(
                title: _buildPageIndicator(index),
              ),
            ),
          ],
        ),
      ));
      index++;
    }
    return pages;
  }

  Widget _buildPageIndicator(int activePage) {
    List<Widget> list = [];
    for (int i = 0; i < widget.exerciseData.length; i++) {
      list.add(i == activePage ? dot_indicator(true) : dot_indicator(false));
    }

    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: list,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.black,
        title: const Text(''),
      ),
      body: PageView(
        controller: _controller,
        children: generatePages(),
      ),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }
}
