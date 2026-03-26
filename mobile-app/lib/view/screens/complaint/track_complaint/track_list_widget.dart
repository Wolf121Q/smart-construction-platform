import 'dart:convert';

import 'package:dha_ctt_app/view/screens/complaint/track_complaint/track_detail.dart';
import 'package:dha_ctt_app/view/screens/complaint/track_complaint/complaint_detail_widget.dart';
import 'package:dha_ctt_app/view/widgets/dialogs/alert_dialogs.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class TrackListWidget extends StatefulWidget {
  final String userId;
  final String trackDay;
  final String trackTime;
  final String trackRefNo;
  final String trackComplainStatus;
  final String category;
  final String subCategory;
  final List<String> ComplaintlistIds;

  final Color colorComplait;
  final int index;

  const TrackListWidget({
    required this.ComplaintlistIds,
    required this.userId,
    required this.trackRefNo,
    required this.trackDay,
    required this.trackTime,
    required this.trackComplainStatus,
    required this.category,
    required this.subCategory,
    required this.colorComplait,
    required this.index,
  });

  @override
  State<TrackListWidget> createState() => _TrackListWidgetState();
}

class _TrackListWidgetState extends State<TrackListWidget> {
  @override
  Widget build(BuildContext context) {
    double scWidth = MediaQuery.of(context).size.width;
    double scHeight = MediaQuery.of(context).size.height;

    String complaintStatus = "Re-open";
    String comment = '';
    String feedback = "";
    TextEditingController comntController = TextEditingController();

    bool isComplaitDetailVisible = false;

    ///------Reopening Complaint---------///

    Future<void> ReopenComplaint(String uid, String comment) async {
      // Define the API endpoint
      final apiUrl = 'http://65.109.233.187/api/complaint/complaint_reopen';

      // Retrieve the authentication token from shared preferences
      final prefs = await SharedPreferences.getInstance();
      final authToken = prefs.getString('longToken');
      final Map<String, dynamic> data = {
        'uid': uid,
        'comment': comment,
      };
      final jsonData = jsonEncode(data);

      try {
        final response = await http.post(
          Uri.parse(apiUrl),
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer $authToken',
          },
          body: jsonData,
        );

        if (response.statusCode == 200) {
          final responseData = jsonDecode(response.body);
          final message = responseData['message'];
          funToast(message, Colors.green);
          print('Response Message: $message');
        } else {
          print('Request failed with status: ${response.statusCode}');
          print('Error message: ${response.body}');
        }
      } catch (error) {
        print('Error: $error');
      }
    }

    return ElevatedButton(
      style: ElevatedButton.styleFrom(
          elevation: 0,
          padding: EdgeInsets.all(0),
          backgroundColor: Colors.transparent),
      onPressed: () {
        Navigator.push(
            context,
            MaterialPageRoute(
                builder: (context) => CompalintDetailWidget(
                      userId: widget.userId,
                    )));
      },
      child: Column(
        children: [
          TrackDetail(
            trackRefNo: widget.trackRefNo,
            trackTime: widget.trackTime,
            trackComplainStatus: widget.trackComplainStatus,
            category: widget.category,
            subCategory: widget.subCategory,
            colorComplait: widget.colorComplait,
            index: widget.index,
          ),
        ],
      ),
    );
  }
}
