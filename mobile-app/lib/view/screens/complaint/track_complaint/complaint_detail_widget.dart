import 'dart:convert';
import 'package:connectivity/connectivity.dart';
import 'package:dha_ctt_app/constant.dart';
import 'package:dha_ctt_app/model/resources/string_manager.dart';
import 'package:dha_ctt_app/model/shared_preferences/share_pref_api_function.dart';
import 'package:dha_ctt_app/view/screens/complaint/update_complaint/update_complaint.dart';
import 'package:dha_ctt_app/view/widgets/app_bar/custom_app_bar.dart';
import 'package:dha_ctt_app/view/widgets/dialogs/custom_dialog.dart';
import 'package:dha_ctt_app/view/widgets/dialogs/custom_toast.dart';
import 'package:dha_ctt_app/view/widgets/track_complaint_detail/complait_detail_visible.dart';
import 'package:dha_ctt_app/view/widgets/track_complaint_detail/track_complaint_detail_action.dart';

import 'package:dha_ctt_app/view_model/view_models/complaint_state_model/complaint_list_long_detail_model.dart';

import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class CompalintDetailWidget extends StatefulWidget {
  final String userId;

  const CompalintDetailWidget({
    required this.userId,
  });

  @override
  State<CompalintDetailWidget> createState() => _CompalintDetailWidgetState();
}

class _CompalintDetailWidgetState extends State<CompalintDetailWidget> {
  //track variales
  List<ComplaintDetailModel> complaintListDetailModel = [];

  // List<ComplaintDetailModel> complaintListDetailModel = [];
  List<ComplaintDetailModel> complaintListDetailModelUpdated = [];

  bool isComplaitDetailVisible = false;

  String uid1 = "";
  String ratingg = "";
  String feedback = "";
  String lat = '0.0';
  String lng = '0.0';
  String status = '';
  List<String> permissions = [];
  bool rateYes = false;
  bool ratePartialy = false;
  bool rateNo = false;

  TextEditingController textEditingController = TextEditingController();
  String appBaseUrl = AppStrings.appBaseUrl;
  String appOwncomplaintActionList = AppStrings.COMPLAINT_ACTION_LIST_DETAILS;
  String appOwncomplaintActionCommentList =
      AppStrings.COMPLAINT_ACTION_COMMENTS_DETAILS;

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    print("Id Check for 2 : ${widget.userId}");
    _loadPermissions();
    //
    // storeComplaintDetailData(widget.userId);
    // storeComplaintDetailsData()
    getStoredComplaintDetailsFromSharedPreferences(widget.userId);

    // getOthersComplaintListDataFromSharedPreferences();
  }

  Future<void> _loadPermissions() async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    setState(() {
      permissions = prefs.getStringList('permissions') ?? [];
      if (permissions.isNotEmpty) {
        print('Permissions list is not empty: $permissions');
        // Do something with the permissions list
      } else {
        print('Permissions list is empty.');
      }
    });
  }

  Future<bool> isInternetConnect() async {
    var connectivityResult = await (Connectivity().checkConnectivity());
    return connectivityResult != ConnectivityResult.none;
  }

  Future<ComplaintDetailModel?> getStoredComplaintDetailsFromSharedPreferences(
      String userId) async {
    print('First Id to gett details run  ${userId}');
    try {
      final SharedPreferences prefs = await SharedPreferences.getInstance();

      // Retrieve the stored data for the specific user
      final String? storedJsonData =
          prefs.getString('complaintDetailsData_$userId');

      if (storedJsonData != null) {
        print('First Id to get data ${storedJsonData}');
        try {
          final Map<String, dynamic> jsonMap = jsonDecode(storedJsonData);

          final ComplaintDetailModel? complaintDetailModel =
              ComplaintDetailModel.fromJson(jsonMap);

          if (complaintDetailModel != null) {
            final List<ComplaintAction>? dataArray =
                complaintDetailModel.dataArray.complaintActions;

            if (dataArray != null && dataArray.isNotEmpty) {
              // Handle your dataArray here
            } else {
              print('DataArray is null or empty');
            }
            print('DataArray complaintDetailModel ' +
                complaintDetailModel.toString());
            return complaintDetailModel;
          } else {
            print('ComplaintDetailModel is null');
          }
        } catch (e) {
          print('Error decoding JSON: $e');
          return null;
        }
      } else {
        print('First Id to get data empty ${storedJsonData}');
        // Handle the case where no data is found
        return null;
      }
    } catch (e) {
      print("Error retrieving stored data: $e");
      return null;
    }
    return null;
  }

  // Retrieve data from SharedPreferences

// Future<ComplaintDetailModel?> getStoredComplaintDetailsFromSharedPreferences(String userId) async {
//   try {
//     final SharedPreferences prefs = await SharedPreferences.getInstance();

//     // Retrieve the stored data for the specific user
//     final String? storedjsonData= prefs.getString('complaintDetailsData_$userId');

//      if (storedjsonData != null) {
//       try {
//         final Map<String, dynamic> jsonMap = jsonDecode(storedjsonData);
//    print('Decoded JSON: $ComplaintDetailModel');
//         return ComplaintDetailModel.fromJson(jsonMap);

//       } catch (e) {
//         print('Error decoding JSON: $e');
//         return null;
//       }
//     } else {
//       // Handle the case where no data is found
//       return null;
//     }
//   } catch (e) {
//     print("Error retrieving stored data: $e");
//     return null;
//   }
// }

  @override
  Widget build(BuildContext context) {
    double scWidth = MediaQuery.of(context).size.width;
    double scHeight = MediaQuery.of(context).size.height;

    String complaintId = "";

    return Scaffold(
      appBar: CustomAppBar(
          navFunction: () {
            Navigator.of(context).pop();
          },
          lastIcon: Icons.info_outline,
          infoFunction: () {
            CustomDialog(context);
          }),
      body: Container(
        color: drakGreyColor,
        height: scHeight,
        alignment: Alignment.center,
        child: FutureBuilder<ComplaintDetailModel?>(
            future:
                getStoredComplaintDetailsFromSharedPreferences(widget.userId),
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) {
                return Center(child: CircularProgressIndicator());
              } else if (snapshot.hasError) {
                return Center(child: Text('Error: ${snapshot.error}'));
              } else if (snapshot.data == null) {
                return Center(child: Text('Error: ${snapshot.data}'));
              } else {
                final complaintLongModel = snapshot.data!;

                return SingleChildScrollView(
                  child: Container(
                    color: drakGreyColor,
                    height: scHeight,
                    // margin: EdgeInsets.symmetric(horizontal: marginLR),
                    child: Stack(
                      alignment: Alignment.bottomCenter,
                      clipBehavior: Clip.antiAlias,
                      children: [
                        Container(
                          height: scHeight,
                          child: Column(
                            children: [
                              ComplaintDetailVisibile(
                                ref: complaintLongModel
                                    .dataArray.complaint.serialNumber,
                                complainCat: complaintLongModel
                                    .dataArray.complaint.category,
                                subCat: complaintLongModel
                                    .dataArray.complaint.subcategory,
                                status: complaintLongModel
                                    .dataArray.complaint.status,
                                complaintDate: complaintLongModel
                                    .dataArray.complaint.createdOn,
                                area:
                                    complaintLongModel.dataArray.complaint.area,
                                percentage: complaintLongModel
                                    .dataArray.complaint.progress
                                    .toString(),
                              ),
                              Container(
                                alignment: Alignment.center,
                                width: scWidth,
                                margin: EdgeInsets.symmetric(
                                    horizontal: marginLR - 5),
                                padding: EdgeInsets.symmetric(vertical: 5),
                                // color: appcolor,
                                child: GestureDetector(
                                  onTap: () {},
                                  child: Text(
                                    "Action",
                                    style: TextStyle(
                                        color: appcolor,
                                        fontSize: smFontSize,
                                        fontWeight: FontWeight.bold),
                                  ),
                                ),
                              ),
                              Container(
                                height: scHeight / 2.5,
                                child: SingleChildScrollView(
                                  child: ListView.builder(
                                    scrollDirection: Axis.vertical,
                                    shrinkWrap: true,
                                    physics: NeverScrollableScrollPhysics(),
                                    itemBuilder: (BuildContext context, int i) {
                                      complaintId = complaintLongModel.dataArray
                                          .complaintActions[i].complaint;
                                      storeComplaintDetailComentsData(
                                          complaintLongModel.dataArray
                                              .complaintActions[i].id);
                                      print('Id for 3rd api' +
                                          complaintLongModel.dataArray
                                              .complaintActions[i].id);
                                      return TrackComplaintDetailAction(
                                        id: complaintLongModel
                                            .dataArray.complaintActions[i].id,
                                        status: complaintLongModel.dataArray
                                            .complaintActions[i].status,
                                        color: complaintLongModel.dataArray
                                            .complaintActions[i].color,
                                        actionDate: complaintLongModel.dataArray
                                            .complaintActions[i].createdOn,
                                        commet: complaintLongModel.dataArray
                                            .complaintActions[i].description,
                                        complaintId: complaintLongModel
                                            .dataArray
                                            .complaintActions[i]
                                            .complaint,
                                      );
                                    },
                                    itemCount: complaintLongModel
                                        .dataArray.complaintActions.length,
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                );
              }
            }),
      ),
      // floatingActionButton: permissions.contains('add_complaint')
      //     ? FloatingActionButton(
      //         onPressed: () async {
      //           bool internetConnected = await isInternetConnect();

      //           if (internetConnected) {
      //             Navigator.push(
      //               context,
      //               MaterialPageRoute(
      //                 builder: (context) => UpdateComplaint(
      //                   userId: complaintId,
      //                 ),
      //               ),
      //             );
      //           } else {
      //             funToast("No Internet Connectivity! ", appcolor);
      //           }
      //         },
      //         backgroundColor: appcolor,
      //         shape: CircleBorder(),
      //         child: const Icon(
      //           Icons.edit,
      //           color: dfColor,
      //         ),
      //       )
      //     : Container(), // empty box if no permission

      floatingActionButton: permissions.contains('change_complaint')
          ? FloatingActionButton(
              onPressed: () async {
                bool internetConnected = await isInternetConnect();

                if (internetConnected) {
                  Navigator.push(
                      context,
                      MaterialPageRoute(
                          builder: (context) => UpdateComplaint(
                                userId: complaintId,
                              )));
                } else {
                  funToast("No Internet Connectivity! ", appcolor);
                }
              },
              backgroundColor: appcolor,
              shape: CircleBorder(),
              child: const Icon(
                Icons.edit,
                color: dfColor,
              ),
            )
          : Container(), // empty box if no permission
    );
  }
}

class IconTextWidget extends StatelessWidget {
  const IconTextWidget({
    super.key,
    required this.text,
    required this.imageIcon,
    required this.color,
  });
  final String text;
  final String imageIcon;
  final Color color;

  @override
  Widget build(BuildContext context) {
    double scWidth = MediaQuery.of(context).size.width;
    double scHeight = MediaQuery.of(context).size.height;
    return Container(
      child: Column(
        children: [
          Container(
            height: scHeight / 20,
            child: Image.asset(
              imageIcon,
              width: scWidth / 15,
              color: color,
            ),
          ),
          Container(
            alignment: Alignment.center,
            width: scWidth / 2.5,
            child: Text(
              text,
              style: TextStyle(
                  fontSize: 15, fontWeight: FontWeight.w500, color: color),
              overflow: TextOverflow.ellipsis,
              softWrap: true,
            ),
          ),
        ],
      ),
    );
  }
}
