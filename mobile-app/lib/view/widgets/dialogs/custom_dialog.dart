import 'dart:ui';

import 'package:awesome_dialog/awesome_dialog.dart';
import 'package:dha_ctt_app/constant.dart';
import 'package:dha_ctt_app/view/screens/complaint/new_complaint/new_complaint.dart';
import 'package:dha_ctt_app/view/screens/qa_complaint/qa_complaint.dart';
import 'package:dha_ctt_app/view/widgets/dialogs/custom_toast.dart';
import 'package:flutter/material.dart';
import 'package:flutter_phone_direct_caller/flutter_phone_direct_caller.dart';

Future CustomDialog(BuildContext context) {
  return AwesomeDialog(
    context: context,
    dialogType: DialogType.question,

    animType: AnimType.topSlide,
    dialogBorderRadius: BorderRadius.circular(50),
    headerAnimationLoop: false,
    padding: EdgeInsets.symmetric(horizontal: 25, vertical: 12),
    descTextStyle: TextStyle(
      fontWeight: FontWeight.w400,
    ),
    title: 'Help',
    desc:
        'If you have any technical queries, you\nmay contact our technical support team\nat 2525 (Dial 4)',

    // showCloseIcon: true,
    btnCancelOnPress: () {
      Navigator.of(context).pop(); // This will close the dialog
    },
    btnOkOnPress: () {
      FlutterPhoneDirectCaller.callNumber('2525');
    }, // Replace with your phone number},
    btnOk: GestureDetector(
      onTap: () {
        // Navigator.of(context).pop(); // This will close the dialog
        FlutterPhoneDirectCaller.callNumber('2525');
      },
      child: CircleAvatar(
          radius: 20,
          backgroundColor: Colors.green,
          child: Icon(
            Icons.phone,
            color: dfColor,
          )),
    ),
    btnCancel: GestureDetector(
      onTap: () {
        Navigator.of(context).pop(); // This will close the dialog
      },
      child: Image.asset(
        "asserts/icons/cross.png",
        height: 40,
      ),
    ),
  ).show();
}

Future<void> showTwoSelectionDialog(BuildContext context,
    {required selectedAreaList, required areaId}) async {
  double scWidth = MediaQuery.of(context).size.width;
  double scHeight = MediaQuery.of(context).size.height;

  return showDialog(
    context: context,
    barrierDismissible:
        false, // Set to false to prevent dismissal on outside click
    builder: (BuildContext context) {
      return Stack(
        alignment: Alignment.center,
        children: [
          // Blurred background
          BackdropFilter(
            filter: ImageFilter.blur(sigmaX: 5.0, sigmaY: 5.0),
            child: Container(),
          ),
          // Your AlertDialog
          AlertDialog(
            backgroundColor: Colors.transparent, // Set to transparent
            alignment: Alignment.center,
            shadowColor: Colors.black,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(roundCardView),
            ),
            elevation: 0,
            clipBehavior: Clip.antiAlias,
            content: Container(
                // margin: EdgeInsets.symmetric(horizontal: 15, vertical: 15),
                padding: EdgeInsets.only(bottom: 25),
                decoration: BoxDecoration(
                  border: Border.all(
                    width: 0.1, // Set the border width
                  ),
                  borderRadius:
                      BorderRadius.circular(50), // Set the border radius
                  color: appcolor.withOpacity(1),
                ),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Container(
                      alignment: Alignment.center,
                      width: scWidth,
                      margin: EdgeInsets.only(top: 0),

                      padding: EdgeInsets.all(0.0), // Adjust padding as needed
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          GestureDetector(
                            onTap: () {
                              Navigator.pop(context); // Dismiss the dialog
                            },
                            child: Container(
                              alignment: Alignment.centerRight,
                              // margin: EdgeInsets.only(top: 10.0),
                              child: CircleAvatar(
                                backgroundColor: dfColor,
                                radius: scWidth /
                                    25, // Adjust radius based on your design
                                child: Icon(
                                  Icons.close_outlined,
                                  size: scWidth / 15,
                                  color: Colors.red,
                                  weight: 52, // Change icon color
                                ),
                              ),
                            ),
                          ),
                          Container(
                            margin: EdgeInsets.only(bottom: marginLR),
                            child: Text(
                              "Select Category",
                              textAlign: TextAlign.center,
                              style: TextStyle(
                                fontSize: scWidth / 23,
                                fontWeight: FontWeight.w900,
                                color: dfColor, // Change to your text color
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                    Container(
                      alignment: Alignment.center,
                      width: scWidth,
                      // padding: EdgeInsets.only(bottom: 100, top: 100),
                      // margin: EdgeInsets.symmetric(vertical: 25, horizontal: 10),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.spaceAround,
                        children: [
                          GestureDetector(
                            onTap: () {
                              Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                      builder: (context) => NewComplaint(
                                            areaId: areaId,
                                          )));
                            },
                            child: Container(
                              margin: EdgeInsets.all(marginSet),
                              width: scWidth / 2.1,
                              // height: scHeight / 9,
                              child: Card(
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(
                                      roundCardView + marginLR),
                                ),
                                elevation: 4,
                                color: dfColor, // Change to your card color
                                child: Padding(
                                  padding: const EdgeInsets.symmetric(
                                    horizontal: 2,
                                    vertical: 20,
                                  ),
                                  child: Column(
                                    mainAxisSize: MainAxisSize.min,
                                    children: [
                                      // Icon(
                                      //   Icons.run_circle_rounded,
                                      //   size: scWidth / 15,
                                      //   color:
                                      //       appcolor, // Change to your icon color
                                      // ),
                                      Image.asset(
                                        "asserts/ctt_icons/new_complaint.png",
                                        width: scWidth / 15,
                                        color: appcolor,
                                      ),
                                      SizedBox(height: 8),
                                      Text(
                                        "COMPLAINT",
                                        textAlign: TextAlign.center,
                                        style: TextStyle(
                                          fontSize: scWidth / 30,
                                          fontWeight: FontWeight.w800,
                                          color:
                                              appcolor, // Change to your text color
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                              ),
                            ),
                          ),
                          GestureDetector(
                            onTap: () {
                              if (selectedAreaList) {
                                Navigator.push(
                                    context,
                                    MaterialPageRoute(
                                        builder: (context) => QACheckList(
                                              areaId: areaId,
                                            )));
                              } else {
                                funToast(
                                    "   Area selection is insufficient.\nPlease select the complete area.",
                                    applightcolor);
                              }
                            },
                            child: Container(
                              width: scWidth / 2.1,
                              margin: EdgeInsets.all(marginSet),
                              //  height: scHeight / 9,
                              child: Card(
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(
                                      roundCardView + marginLR),
                                ),
                                elevation: selectedAreaList ? 4 : 0,
                                color: selectedAreaList
                                    ? dfColor
                                    : drakGreyColor1, // Change to your card color
                                child: Padding(
                                  padding: const EdgeInsets.symmetric(
                                    horizontal: 2,
                                    vertical: 20,
                                  ),
                                  child: Column(
                                    mainAxisSize: MainAxisSize.min,
                                    children: [
                                      Icon(
                                        Icons.list_alt_rounded,
                                        size: scWidth / 13,
                                        color: selectedAreaList
                                            ? appcolor
                                            : applightcolor, // Change to your icon color
                                      ),
                                      SizedBox(height: 8),
                                      Text(
                                        "QA CHECKLIST",
                                        textAlign: TextAlign.center,
                                        style: TextStyle(
                                          fontSize: scWidth / 30,
                                          fontWeight: FontWeight.w800,
                                          color: selectedAreaList
                                              ? appcolor
                                              : applightcolor, // Change to your text color
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                )),
            actions: <Widget>[],
          ),
        ],
      );
    },
  );
}

Future CustomAlertDialog(BuildContext context,
    {required title,
    required dialogType,
    required description,
    required function}) {
  return AwesomeDialog(
    context: context,
    dialogType: dialogType,
    animType: AnimType.bottomSlide,
    dialogBorderRadius: BorderRadius.circular(50),
    headerAnimationLoop: false,
    padding: EdgeInsets.symmetric(horizontal: 25, vertical: 12),
    descTextStyle: TextStyle(
      fontSize: dfFontSize,
      fontWeight: FontWeight.w500,
    ),
    btnOkColor: appcolor,
    title: title,
    desc: description,
    titleTextStyle: TextStyle(
      fontSize: lgFontSize,
      fontWeight: FontWeight.bold,
    ),

    btnOkOnPress: function, // Replace with your phone number},
    btnOkText: "Okay",
  ).show();
}

Future<void> downloadAllComplaintDialog(
  BuildContext context, {
  required fun,
  required isDownLoading,
}) async {
  double scWidth = MediaQuery.of(context).size.width;
  double scHeight = MediaQuery.of(context).size.height;

  return showDialog(
    context: context,
    barrierDismissible:
        false, // Set to false to prevent dismissal on outside click
    builder: (BuildContext context) {
      return Stack(
        alignment: Alignment.center,
        children: [
          // Blurred background
          BackdropFilter(
            filter: ImageFilter.blur(sigmaX: 5.0, sigmaY: 5.0),
            child: Container(),
          ),
          // Your AlertDialog
          AlertDialog(
            backgroundColor: Colors.transparent, // Set to transparent
            alignment: Alignment.center,
            shadowColor: Colors.black,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(roundCardView),
            ),
            elevation: 0,
            clipBehavior: Clip.antiAlias,
            content: Container(
                // margin: EdgeInsets.symmetric(horizontal: 15, vertical: 15),
                padding: EdgeInsets.only(bottom: 25),
                decoration: BoxDecoration(
                  border: Border.all(
                    width: 0.1, // Set the border width
                  ),
                  borderRadius:
                      BorderRadius.circular(50), // Set the border radius
                  color: appcolor.withOpacity(1),
                ),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Container(
                      alignment: Alignment.center,
                      width: scWidth,
                      margin: EdgeInsets.only(top: 0),

                      padding: EdgeInsets.all(0.0), // Adjust padding as needed
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          GestureDetector(
                            onTap: () {
                              Navigator.pop(context); // Dismiss the dialog
                            },
                            child: Container(
                              alignment: Alignment.centerRight,
                              // margin: EdgeInsets.only(top: 10.0),
                              child: CircleAvatar(
                                backgroundColor: dfColor,
                                radius: scWidth /
                                    25, // Adjust radius based on your design
                                child: Icon(
                                  Icons.close_outlined,
                                  size: scWidth / 15,
                                  color: Colors.red,
                                  weight: 52, // Change icon color
                                ),
                              ),
                            ),
                          ),
                          Container(
                            margin: EdgeInsets.only(bottom: marginLR),
                            child: Text(
                              "All History Download!",
                              textAlign: TextAlign.center,
                              style: TextStyle(
                                fontSize: scWidth / 23,
                                fontWeight: FontWeight.w900,
                                color: dfColor, // Change to your text color
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                    Container(
                      alignment: Alignment.center,
                      width: scWidth,
                      // padding: EdgeInsets.only(bottom: 100, top: 100),
                      // margin: EdgeInsets.symmetric(vertical: 25, horizontal: 10),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.spaceAround,
                        children: [
                          Container(
                            margin: EdgeInsets.all(marginSet),
                            width: scWidth / 2.1,
                            // height: scHeight / 9,
                            child: Padding(
                              padding: const EdgeInsets.symmetric(
                                horizontal: 2,
                                vertical: 10,
                              ),
                              child: Column(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  Text(
                                    "When you click the 'Download' button, your complaint history will begin downloading, and you can track the progress on the complaint list page. You have the option to stop the download at any time during the process coming back on this page.",
                                    textAlign: TextAlign.center,
                                    style: TextStyle(
                                      fontSize: scWidth / 35,
                                      fontWeight: FontWeight.w500,
                                      color:
                                          dfColor, // Change to your text color
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ),
                          GestureDetector(
                            onTap: fun,
                            //funToast('clicked', Colors.red);

                            child: Container(
                              width: scWidth / 1.8,
                              margin: EdgeInsets.all(marginSet),
                              //  height: scHeight / 9,
                              child: Card(
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(
                                      roundCardView + marginLR),
                                ),
                                elevation: 0,
                                color:
                                    drakGreyColor1, // Change to your card color
                                child: Padding(
                                  padding: const EdgeInsets.symmetric(
                                    horizontal: 2,
                                    vertical: 10,
                                  ),
                                  child: Row(
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    mainAxisSize: MainAxisSize.min,
                                    children: [
                                      Text(
                                        isDownLoading ? "Cancel" : "Download",
                                        textAlign: TextAlign.center,
                                        style: TextStyle(
                                          fontSize: scWidth / 30,
                                          fontWeight: FontWeight.w800,
                                          color:
                                              applightcolor, // Change to your text color
                                        ),
                                      ),
                                      SizedBox(height: 8),
                                      Icon(
                                        Icons.downloading_sharp,
                                        size: scWidth / 13,
                                        color:
                                            appcolor, // Change to your icon color
                                      ),
                                    ],
                                  ),
                                ),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                )),
            actions: <Widget>[],
          ),
        ],
      );
    },
  );
}
