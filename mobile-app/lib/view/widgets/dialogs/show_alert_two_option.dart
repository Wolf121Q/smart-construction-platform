import 'package:flutter/material.dart';

Future<void> _showTwoSelectionDialog(BuildContext context) async {
    return showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('Select an Option'),
          content: Text('Choose one of the following options:'),
          actions: <Widget>[
            TextButton(
              onPressed: () {
                Navigator.of(context).pop(); // Close the dialog
                // Perform action for Option 1
                print('Option 1 selected');
              },
              child: Text('Option 1'),
            ),
            TextButton(
              onPressed: () {
                Navigator.of(context).pop(); // Close the dialog
                // Perform action for Option 2
                print('Option 2 selected');
              },
              child: Text('Option 2'),
            ),
          ],
        );
      },
    );
  }
