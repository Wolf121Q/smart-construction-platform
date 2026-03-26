import 'dart:convert';

import 'package:dha_ctt_app/constant.dart';
import 'package:dha_ctt_app/view/widgets/track_complaint_detail/complaint_detail_image.dart';
import 'package:dha_ctt_app/view_model/view_models/complaint_state_model/complaint_action_comments.dart';
import 'package:http/http.dart' as http;

import 'package:dha_ctt_app/model/shared_preferences/share_pref_api_function.dart';
import 'package:dha_ctt_app/view_model/utils/color_widget.dart';
import 'package:dha_ctt_app/view_model/utils/date_formats.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class TrackComplaintDetailAction extends StatefulWidget {
  final String status;
  final String actionDate;
  final String commet;
  final String color;
  final String id;
  final String complaintId;

  const TrackComplaintDetailAction({
    required this.id,
    required this.status,
    required this.color,
    required this.actionDate,
    required this.commet,
    required this.complaintId,
  });

  @override
  State<TrackComplaintDetailAction> createState() =>
      _TrackComplaintDetailActionState();
}

class _TrackComplaintDetailActionState
    extends State<TrackComplaintDetailAction> {
  bool isComplaitDetailVisible = false;
  bool isComplaitDetailImage = false;
  List<ComplaintActionCommentsItemModel> complaintCommentsDetailModel = [];
  List<ComplaintActionCommentsItemModel> complaintCommentsDetailModelUpdated =
      [];
  List<ComplaintActionCommentsItemModel>? others_complaint_list_model;
  List<ComplaintActionCommentsItemModel> comlintDetailListToGetImage = [];
  // List<ComplaintActionCommentsItemModel> complaint_action_comments_list = [];
  // List<ImageDataArray> complaint_action_images_list = [];

  //getting complaint comnet data from api
// Function to retrieve status from SharedPreferences and populate the list
  Future<void> getOthersComplaintCommentsDataFromSharedPreferences() async {
    try {
      final SharedPreferences prefs = await SharedPreferences.getInstance();
      final String? trackComplaintListDataSerialzed =
          prefs.getString('complaintCommentsDetailsData');

      if (trackComplaintListDataSerialzed != null &&
          trackComplaintListDataSerialzed.isNotEmpty) {
        final List<dynamic> dataArray =
            jsonDecode(trackComplaintListDataSerialzed);

        complaintCommentsDetailModel = dataArray
            .map((json) => ComplaintActionCommentsItemModel.fromJson(json))
            .toList();

        // Update the lists if needed

        List<ComplaintActionCommentsItemModel> updatedDashboardList = [];

        complaintCommentsDetailModel.forEach((status) {
          updatedDashboardList.add(status);
        });

        setState(() {
          if (complaintCommentsDetailModelUpdated.isNotEmpty)
            complaintCommentsDetailModelUpdated.clear();

          complaintCommentsDetailModelUpdated = updatedDashboardList;

          // Update the status list
          print(
              'Data fro image 1 =  ${complaintCommentsDetailModelUpdated[0].uid} ');
        });
      } else {
        print('No Dashboard data found in SharedPreferences.');
      }
    } catch (e) {
      print('Error retrieving Dashboard data from SharedPreferences: $e');
    }
  }

  Future<void> storeComplaintDetailComentsData(String userId) async {
    try {
      final SharedPreferences prefs = await SharedPreferences.getInstance();
      final String token = prefs.getString('access_token') ?? '';

      Map<String, String> headers = {
        'Authorization': 'Bearer $token',
      };

      final response = await http.get(
        Uri.parse(appBaseUrl + complaintCommnentsDetails + userId),
        headers: headers,
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> data = jsonDecode(response.body);
        final List<dynamic> dataArray = data['data_array'];

        others_complaint_list_model = dataArray
            .map((jsonData) =>
                ComplaintActionCommentsItemModel.fromJson(jsonData))
            .toList();
        comlintDetailListToGetImage == others_complaint_list_model;

        // final List<Map<String, dynamic>> serializedData =
        //     others_complaint_list_model
        //         .map((othersComlaintItemItem) => othersComlaintItemItem.toJson())
        //         .toList();

        setState(() {
          comlintDetailListToGetImage == others_complaint_list_model;
        });

        //Save Dashboard data
        // saveDashboardChatModelToPrefs(jsonData);
        //
        print(
            "API request for Complaint Detail to get image size: ${others_complaint_list_model?.length.toString()}");

        // await prefs.setString(
        //     'complaintCommentsDetailsData', jsonEncode(serializedData));
      } else {
        print(
            "API request for Complaint Detail failed with status: ${response.statusCode}.");
      }
    } catch (e) {
      print("Error storing Complaint Detail data: $e");
    }
  }

  // Future<ComplaintActionCommentsDataModel>
  //     fetchComplaintActionCommentsDataModel() async {
  //   final SharedPreferences prefs = await SharedPreferences.getInstance();
  //   final String token = prefs.getString('access_token') ?? '';

  //   Map<String, String> headers = {
  //     'Authorization': 'Bearer $token',
  //   };

  //   String OWN_COMPLAINT_ACTION_COMMENTS =
  //       appBaseUrl + AppStrings.COMPLAINT_ACTION_COMMENTS_DETAILS;

  //   final response = await http.get(
  //       Uri.parse(OWN_COMPLAINT_ACTION_COMMENTS + widget.id),
  //       headers: headers);

  //   if (response.statusCode == 200) {
  //     final Map<String, dynamic> responseData = json.decode(response.body);

  //     //   print('ComplaintActionCommentsDataModel= ' + responseData.toString());

  //     return ComplaintActionCommentsDataModel.fromJson(responseData);
  //   } else {
  //     throw Exception('Failed to load data');
  //   }
  // }

  @override
  void initState() {
    // TODO: implement initState   'complaintCommentsDetailsData'
    super.initState();

    // fetchComplaintActionCommentsDataModel();
  }

  @override
  Widget build(BuildContext context) {
    double scWidth = MediaQuery.of(context).size.width;
    double scHeight = MediaQuery.of(context).size.height;

    String? complaintImageId;
    return Container(
      child: Column(
        children: [
          Container(
            width: scWidth,
            margin:
                EdgeInsets.symmetric(vertical: marginLR, horizontal: marginLR),
            padding: EdgeInsets.symmetric(vertical: 5, horizontal: 0),
            decoration: BoxDecoration(
                color: dfColor, borderRadius: BorderRadius.circular(12)),
            child: Container(
              margin: EdgeInsets.symmetric(
                  horizontal: marginLR + marginLR, vertical: 5),
              child: Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Container(
                        padding:
                            EdgeInsets.symmetric(vertical: 5, horizontal: 10),
                        decoration: BoxDecoration(
                            color: HexColor.fromHex(widget.color),
                            borderRadius: BorderRadius.circular(12)),
                        child: Text(
                          widget.status,
                          style: TextStyle(
                              fontSize: 13,
                              color: appcolor,
                              fontWeight: FontWeight.w700),
                        ),
                      ),
                      isComplaitDetailVisible == false
                          ? Container(
                              padding: const EdgeInsets.symmetric(
                                  vertical: 5, horizontal: 10),
                              child: Text(
                                formatDate(widget.actionDate),
                                style: TextStyle(
                                    fontSize: 13,
                                    color: appcolor,
                                    fontWeight: FontWeight.w700),
                              ),
                            )
                          : InkWell(
                              onTap: () {
                                setState(() {
                                  print("show image clicked");
                                  if (isComplaitDetailImage == false) {
                                    isComplaitDetailImage = true;
                                  } else {
                                    isComplaitDetailImage = false;
                                  }
                                });
                              },

                              child: Image.asset(
                                'asserts/gifs/attachments_animation.gif',
                                width: scWidth / 10,
                              ),
                              //  Icon(
                              //   Icons.attach_file,
                              //   color: appcolor,
                              // ),
                            ),
                    ],
                  ),
                  Container(
                    margin:
                        EdgeInsets.symmetric(vertical: 5, horizontal: marginLR),
                    child: Divider(
                      color: appcolor,
                    ),
                  ),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Icon(
                        Icons.subdirectory_arrow_right,
                        color: appcolor,
                      ),
                      InkWell(
                        onTap: () async {
                          if (isComplaitDetailVisible == false) {
                            setState(() {
                              // getOthersComplaintCommentsDataFromSharedPreferences();
                              storeComplaintDetailComentsData(widget.id);
                            });
                            isComplaitDetailVisible = true;
                          } else {
                            isComplaitDetailVisible = false;
                            isComplaitDetailImage = false;
                          }
                        },
                        child: isComplaitDetailVisible == false
                            ? Container(
                                padding: EdgeInsets.symmetric(
                                    vertical: 5, horizontal: 10),
                                decoration: BoxDecoration(
                                    color: appcolor,
                                    borderRadius: BorderRadius.circular(12)),
                                child: Text(
                                  "View More",
                                  style: TextStyle(
                                      fontSize: 13,
                                      color: dfColor,
                                      fontWeight: FontWeight.w700),
                                ),
                              )
                            : SizedBox(
                                width: scWidth / 1.5,
                                child: Text(
                                  widget.commet,
                                  style: TextStyle(
                                      fontSize: 13,
                                      color: appcolor,
                                      fontWeight: FontWeight.w700),
                                ),
                              ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
          isComplaitDetailImage == true
              ? Container(
                  // height: scHeight / 8,
                  child:

                      // FutureBuilder<ComplaintActionCommentsDataModel>(
                      // future: fetchComplaintActionCommentsDataModel(),
                      // builder: (context, snapshot) {
                      //   if (snapshot.connectionState ==
                      //       ConnectionState.waiting) {
                      //     return Center(child: CircularProgressIndicator());
                      //   } else if (snapshot.hasError) {
                      //     return Center(
                      //         child: Text('Error: ${snapshot.error}'));
                      //   } else {
                      // final complaintData = snapshot.data;
                      ListView.builder(
                          scrollDirection: Axis.vertical,
                          shrinkWrap: true,
                          itemCount: others_complaint_list_model != null
                              ? others_complaint_list_model!.length
                              : 0,
                          physics: NeverScrollableScrollPhysics(),
                          itemBuilder: (BuildContext context, int i) {
                            if (others_complaint_list_model != null) {
                              complaintImageId =
                                  others_complaint_list_model![i].id;
                              print('Id For 4 api lentgh ' +
                                  others_complaint_list_model![i]
                                      .id
                                      .toString());

                              return ComplaitDetailImage(
                                  id: others_complaint_list_model![i].id!,
                                  index: i);
                            } else {
                              // Return a placeholder widget or an empty container if the list is null
                              return Container();
                            }
                          }),
                  // ListView.builder(
                  //     scrollDirection: Axis.vertical,
                  //     shrinkWrap: true,
                  //     itemCount: others_complaint_list_model != null
                  //         ? others_complaint_list_model!.length
                  //         : 0,
                  //     physics: NeverScrollableScrollPhysics(),
                  //     itemBuilder: (BuildContext context, int i) {}),
                  //   }
                  // }),
                )
              : Container(),
        ],
      ),
    );
  }
}
