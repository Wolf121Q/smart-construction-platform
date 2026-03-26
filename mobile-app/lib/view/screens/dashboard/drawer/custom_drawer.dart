
import 'package:dha_ctt_app/constant.dart';
import 'package:dha_ctt_app/model/resources/values_manager.dart';
import 'package:dha_ctt_app/view/screens/complaint/track_complaint/other_complaint.dart';
import 'package:dha_ctt_app/view/screens/complaint/track_complaint/track_complaint.dart';
import 'package:dha_ctt_app/view/screens/dashboard/home.dart';
import 'package:dha_ctt_app/view/screens/pending_task/pending_task.dart';
import 'package:get/get.dart';

import 'package:flutter/material.dart';

class CustomDrawer extends StatefulWidget {
  const CustomDrawer({super.key});

  @override
  State<CustomDrawer> createState() => _CustomDrawerState();
}

class _CustomDrawerState extends State<CustomDrawer> {
  late Map<String, dynamic> data1 = {};
  late String longtoken1 = "";
  late String shorttoken1 = "";

  String userName = "";

  String uid1 = "";

  @override
  Widget build(BuildContext context) {
    double scWidth = MediaQuery.of(context).size.width;
    double scHeight = MediaQuery.of(context).size.height;
    return SingleChildScrollView(
      // padding: Platform.isAndroid
      //     ? EdgeInsets.symmetric(vertical: 10.0)
      //     : EdgeInsets.symmetric(vertical: 0.0),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          CircleAvatar(
            backgroundColor: Colors.transparent,
            radius: 80.0,
            child: Container(
                margin: EdgeInsets.only(right: 50),
                child: Image.asset("asserts/icons/app_icon.png")),
          ),
          Container(
            margin: EdgeInsets.only(top: marginLR),
            color: drakGreyColor,
            child: ListTile(
              onTap: () {
                Get.offAll(() => Home());
              },
              title: Container(
                margin: EdgeInsets.only(right: 30),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text(
                      "Home",
                      style: TextStyle(
                          fontSize: dfFontSize, fontWeight: FontWeight.bold),
                    ),
                    Image.asset(
                      "asserts/ctt_icons/home.png",
                      width: AppSize.s24,
                      color: appcolor,
                    ),
                  ],
                ),
              ),
              textColor: appcolor,
              dense: true,
            ),
          ),
          Container(
            margin: EdgeInsets.only(top: marginLR),
            color: drakGreyColor,
            child: ListTile(
              onTap: () {
                Get.offAll(
                  () => TrackComplaints(),
                  arguments: ['Total', 0], // Pass your text data as an argument
                );
              },
              title: Container(
                margin: EdgeInsets.only(right: 30),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      "Track Complaint",
                      style: TextStyle(
                          fontSize: dfFontSize, fontWeight: FontWeight.bold),
                    ),
                    Image.asset(
                      "asserts/ctt_icons/track_complaint.png",
                      width: AppSize.s24,
                      color: appcolor,
                    ),
                  ],
                ),
              ),
              textColor: appcolor,
              dense: true,
            ),
          ),
          Container(
            margin: EdgeInsets.only(top: marginLR),
            color: drakGreyColor,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                ListTile(
                  onTap: () {
                    Get.offAll(
                      () => OtherComplaints(),
                      arguments: [
                        'Total',
                        0
                      ], // Pass your text data as an argument
                    );
                  },
                  title: Container(
                    margin: EdgeInsets.only(right: 30),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          "Other Complaints",
                          style: TextStyle(
                              fontSize: dfFontSize,
                              fontWeight: FontWeight.bold),
                        ),
                        Image.asset(
                          "asserts/ctt_icons/other_complaint1.png",
                          width: AppSize.s24,
                          color: appcolor,
                        ),
                      ],
                    ),
                  ),
                  textColor: appcolor,
                  dense: true,
                ),
              ],
            ),
          ),
          Container(
            margin: EdgeInsets.only(top: marginLR),
            color: drakGreyColor,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                ListTile(
                  onTap: () {
                    Get.offAll(() => PendingTask());
                  },
                  title: Container(
                    margin: EdgeInsets.only(right: 30),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          "Pending Task",
                          style: TextStyle(
                              fontSize: dfFontSize,
                              fontWeight: FontWeight.bold),
                        ),
                        Image.asset(
                          "asserts/ctt_icons/pending_task.png",
                          width: AppSize.s24,
                          color: appcolor,
                        ),
                      ],
                    ),
                  ),
                  textColor: appcolor,
                  dense: true,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
