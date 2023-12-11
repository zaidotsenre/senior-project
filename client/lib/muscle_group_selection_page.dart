import 'package:flutter/material.dart';
import 'exercise_data_page.dart';

class MuscleGroupSelectionPage extends StatelessWidget {
  final List<Map> exerciseData;

  const MuscleGroupSelectionPage(this.exerciseData, {super.key});

  Future<void> _navigateToExerciseData(
      BuildContext context, List<Map> exerciseData) async {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (context) => ExerciseDataPage(exerciseData),
      ),
    );
  }

  String capitalize(String s) {
    return "${s[0].toUpperCase()}${s.substring(1)}";
  }

  List<Widget> generateListTiles(BuildContext context) {
    Set muscles = {};
    for (var entry in exerciseData) {
      muscles.add(entry['target_muscle']);
    }

    List<Widget> listTiles = [];
    for (var muscle in muscles) {
      List<Map> relevantExercises = [];
      for (var exercise in exerciseData) {
        if (exercise['target_muscle'] == muscle) {
          relevantExercises.add(exercise);
        }
      }

      listTiles.add(ListTile(
        leading: Image.asset('assets/icons/$muscle.png'),
        title: Text(capitalize(muscle.replaceFirst(RegExp('_'), ' '))),
        contentPadding: const EdgeInsets.only(
            top: 5.0, bottom: 5.0, left: 20.0, right: 20.0),
        onTap: () {
          _navigateToExerciseData(context, relevantExercises);
        },
      ));
    }

    return listTiles;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        title: const Text('Pick a muscle'),
        backgroundColor: Colors.black,
      ),
      body: ListView(
        children: generateListTiles(context),
      ),
    );
  }
}
