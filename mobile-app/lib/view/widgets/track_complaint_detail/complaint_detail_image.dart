import 'dart:convert';
import 'dart:io';
import 'package:dha_ctt_app/animation/image_zoom_animation.dart';
import 'package:http/http.dart' as http;
import 'package:dha_ctt_app/constant.dart';
import 'package:dha_ctt_app/model/resources/string_manager.dart';
import 'package:dha_ctt_app/model/shared_preferences/share_pref_api_function.dart';
import 'package:dha_ctt_app/view_model/view_models/complaint_state_model/complaint_image_model.dart';
import 'package:flutter/material.dart';
import 'package:insta_image_viewer/insta_image_viewer.dart';
import 'package:shared_preferences/shared_preferences.dart';

class ComplaitDetailImage extends StatefulWidget {
  final String id;
  final int index;
  ComplaitDetailImage({required this.id, required this.index});

  @override
  State<ComplaitDetailImage> createState() => _ComplaitDetailImageState();
}

class _ComplaitDetailImageState extends State<ComplaitDetailImage> {
  // getting data from api own complaint
  Future<ComplaintImageModel> fetchComplaintImageModel() async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    final String token = prefs.getString('access_token') ?? '';

    Map<String, String> headers = {
      'Authorization': 'Bearer $token',
    };

    String OWN_COMPLAINT_ACTION_COMMENTS =
        appBaseUrl + AppStrings.COMPLAINT_ACTION_COMMENTS_IMAGE_DETAILS;
    //  return Center(child: Text('Please Check Your Internet And Try Again'));
    final response = await http.get(
        Uri.parse(OWN_COMPLAINT_ACTION_COMMENTS + widget.id),
        headers: headers);

    if (response.statusCode == 200) {
      final Map<String, dynamic> responseData = json.decode(response.body);

      print('Complaint Action Image Data Model= ' + responseData.toString());

      return ComplaintImageModel.fromJson(responseData);
    } else {
      throw Exception('Failed to load data');
    }
  }

  @override
  void initState() {
    // TODO: implement initState
    super.initState();

    // fetchComplaintImageModel();
    // getOthersComplaintCommentsDataFromSharedPreferences();
    print("Image Id :" + widget.id);
  }

  @override
  Widget build(BuildContext context) {
    double scWidth = MediaQuery.of(context).size.width;
    double scHeight = MediaQuery.of(context).size.height;
    return Container(
      width: scWidth,
      margin: EdgeInsets.symmetric(vertical: marginLR, horizontal: marginLR),
      padding: EdgeInsets.symmetric(vertical: 5, horizontal: 0),
      decoration: BoxDecoration(
          color: dfColor, borderRadius: BorderRadius.circular(12)),
      child: Container(
        alignment: Alignment.center,
        margin: EdgeInsets.symmetric(
          horizontal: marginLR + marginLR,
          vertical: 5,
        ),
        child: Column(
          children: [
            Container(
              // margin: EdgeInsets.only(bottom: 10),
              child: Text(
                "Attachments",
                style: TextStyle(
                    color: appcolor,
                    fontSize: smFontSize,
                    fontWeight: FontWeight.bold),
              ),
            ),

            // ---------testing ------///

            FutureBuilder<ComplaintImageModel>(
              future: fetchComplaintImageModel(),
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return Center(child: CircularProgressIndicator());
                } else if (snapshot.hasError) {
                  return Center(child: Text('No Internet Connection!'));
                } else if (!snapshot.hasData ||
                    snapshot.data!.dataArray.isEmpty) {
                  return Center(child: Text('No image data available.'));
                } else {
                  final complaintData = snapshot.data;
                  String imag_path = AppStrings.appBaseUrlimage +
                      complaintData!.dataArray[widget.index].attachment;
                  print('imag_path $imag_path');
                  return Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      InstaImageViewer(
                        child: Image.network(
                          imag_path,
                          //  complaintData!.dataArray[0].attachment,
                          width: scWidth / 6,
                          errorBuilder: (context, error, stackTrace) {
                            return Text('Error Loading Image!');
                          },
                        ),
                      ),
                    ],
                  );
                }
              },
            )
          ],
        ),
      ),
    );
  }

  ///Custom Dialog
  _showCustomDialog(String imageUrl) {
    showGeneralDialog(
      context: context,
      pageBuilder: (ctx, a1, a2) {
        return Container();
      }, //
      transitionBuilder: (ctx, a1, a2, child) {
        var curve = Curves.easeInOut.transform(a1.value);
        return Transform.scale(
          scale: curve,
          child: AlertDialog(
            titlePadding: EdgeInsets.all(0),
            title: Container(
              alignment: Alignment.topLeft,
              decoration: BoxDecoration(
                color: appcolor,
              ),
              child: IconButton(
                icon: Icon(
                  Icons.cancel_outlined,
                  color: Colors.red,
                ),
                onPressed: () {
                  Navigator.of(context).pop();
                },
              ),
            ),
            contentPadding: EdgeInsets.zero,
            content: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(
                  child: ImageZoomWidget(
                    zoomImage: Image.network(
                      imageUrl,
                      errorBuilder: (context, exception, stackTrace) {
                        return Image.asset("asserts/icons/icon.png");
                      },
                    ),
                  ),
                ),
              ],
            ),
          ),
        );
      },
      transitionDuration: const Duration(milliseconds: 300),
    );
  }
}

class ImageDisplayWidget extends StatelessWidget {
  final String imagePath;

  ImageDisplayWidget({required this.imagePath});

  @override
  Widget build(BuildContext context) {
    return Image.file(
      File(imagePath),
      width: 100.0,
      height: 100.0,
      fit: BoxFit.cover,
    );
  }
}
