import 'dart:convert';

import 'package:awesome_dialog/awesome_dialog.dart';
import 'package:connectivity/connectivity.dart';
import 'package:dha_ctt_app/model/apis/api_client.dart';
import 'package:dha_ctt_app/model/repository/auth_repo.dart';
import 'package:dha_ctt_app/model/shared_preferences/share_pref_api_function.dart';
import 'package:dha_ctt_app/view/screens/complaint/add_area/add_area.dart';
import 'package:dha_ctt_app/view/screens/complaint/track_complaint/other_complaint.dart';
import 'package:dha_ctt_app/view/screens/dashboard/chart/custom_chart.dart';
import 'package:dha_ctt_app/view/widgets/dialogs/custom_toast.dart';
import 'package:dha_ctt_app/view_model/utils/color_widget.dart';
import 'package:dha_ctt_app/view_model/view_models/dashboard_model/dashboard_chat_model.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:get_storage/get_storage.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:shimmer/shimmer.dart';

import '../../../constant.dart';

class Dashboard extends StatefulWidget {
  final String? apiChacker;
  final String? splachChacker;

  Dashboard(this.apiChacker, this.splachChacker);

  @override
  State<Dashboard> createState() => _DashboardState();
}

class _DashboardState extends State<Dashboard> {
  final AuthRepo authRepo = AuthRepo(apiClient: ApiClient());
// Declare a variable to store arguments
  static int _valueUsed = 0;
  static int _valueUsed1 = 0;
  late AnimationController _controller;
  static int? complainStatusCounter = 0;
  static bool isLoading = true; // Set to true initially
  static int? statuses1Count = 0;
  static int? statuses2Count = 0;
  static int? statuses3Count = 0;
  static int? statuses4Count = 0;

  static String? statuses1Colour;
  static String? statuses2Colour;
  static String? statuses3Colour;
  static String? statuses4Colour;

  static String? statuses1Name;
  static String? statuses2Name;
  static String? statuses3Name;
  static String? statuses4Name;
  static String? filterName;
  DateTime? _loginTime;
  bool errorLod = false;

  // int? inProcess = 0;
  // int? closed = 0;
  // int? resolved = 0;
  // int? reOpen = 0;
  // int? total = 0;

  // String? colorinProcess;
  // String? colorclosed;
  // String? colorresolved;
  // String? colorreOpen;
  // String? colortotal;

  String userName = "";
  String email = "";
  int? loginTime;
  List<String> permissions = [];

  var box = GetStorage();
  DashboardChatModel user = DashboardChatModel();

  List<DataItem> dashboardChatModel = [];
  List<DataItem> allDashboardData = [];

  Future<void> loadSessionData() async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    int difference = 0;

    final String? storedUsername = prefs.getString('username');
    final int? storedLoginTime = prefs.getInt('login_time');
    final String? tokenExpiryTime = prefs.getString('token_expiry_time');
    permissions = prefs.getStringList('permissions') ?? [];
    if (permissions.isNotEmpty) {
      print('Permissions list is not empty: $permissions');
      // Do something with the permissions list
    } else {
      print('Permissions list is empty.');
    }

    if (storedUsername != null && storedLoginTime != null) {
      setState(() {
        userName = storedUsername;
        loginTime = storedLoginTime;
        _loginTime = DateTime.fromMillisecondsSinceEpoch(loginTime!);

        if (_loginTime != null) {
          final currentTime = DateTime.now();
          difference = currentTime.difference(_loginTime!).inHours;
        }
      });

      checkConnectivity();

      print('token Expiry Time ' + tokenExpiryTime.toString());
      print('total logged in time ' + difference.toString());
      // Extract the integer part using regular expression
      RegExp regExp = RegExp(r'\d+');
      int? expiryDays =
          int.tryParse(regExp.firstMatch(tokenExpiryTime!)?.group(0) ?? '');

      await Future.delayed(Duration(seconds: 1));
      int i = 0;
      if (errorLod == true &&
          widget.splachChacker == 'splach' &&
          _valueUsed == 0) {
        // Show the dialog to the user
        if (difference >= expiryDays!) {
          print('No Internet availabel');
          _valueUsed = 1;
          print('widget.apiChacker checked ' + widget.splachChacker!);
          AwesomeDialog(
            context: context,
            dialogType: DialogType.info,
            animType: AnimType.bottomSlide,
            title: 'Session Warning!',
            desc:
                'Please connect to the internet to check for session validity!',
            btnCancel: IconButton(
              onPressed: () {
                Navigator.pop(context); // Close the dialog
              },
              icon: Image.asset(
                'asserts/icons/checked.png',
                width: 40,
              ),
              color: Colors.green,
            ),
          ).show();
        }
        print('test AwesomeDialog = ${i++}');
        AwesomeDialog(
          context: context,
          dialogType: DialogType.info,
          animType: AnimType.bottomSlide,
          title: 'No Internet Connection!',
          desc:
              'No active internet connection was found! \n The app will now run in offline mode, for best experience, please connect to the internet!',
          btnCancel: IconButton(
            onPressed: () {
              Navigator.pop(context); // Close the dialog
            },
            icon: Image.asset(
              'asserts/icons/checked.png',
              width: 40,
            ),
            color: Colors.green,
          ),
        ).show();
      }

      print('Internet availabel');
    }
  }

  @override
  void initState() {
    // TODO: implement initState
    super.initState();

    checkConnectivity();
    // loadSessionData();
    storeDashboardChartApitoCheckLoginSession(context);
    // getDashboardChatFromSharedPreferences();
    // isInternetConnect();

    storeDashboardChartApi();
    // checkInternet();
    // getDashboardChatFromSharedPreferences();

    print("api chaker o dashbaourd  Status: ${widget.apiChacker}");

    // isLoading = false;
    if (widget.apiChacker == 'login') {
      storeApiData();
      loadSessionData();
    } else {
      getDashboardChatFromSharedPreferences();

      loadSessionData();
      isLoading = false;
    }
  }

  ///refresh
  Future refresh() async {
    setState(() {
      storeDashboardChartApi();
      getDashboardChatFromSharedPreferences();
      isLoading = false;
    });
  }

  Future<bool> isInternetConnect() async {
    var connectivityResult = await (Connectivity().checkConnectivity());

    return connectivityResult != ConnectivityResult.none;
  }

  Future<void> checkInternet() async {
    errorLod = await isInternetConnect();
  }

  Future<void> storeApiData() async {
    try {
      await storeArealistApi();
      storeCategorieslistApi();
      storeQACategorieslistApi();
      storeStatusApi();
      await storeDashboardChartApi();
      await getDashboardChatFromSharedPreferences();
      isLoading = false;
      storeOthersComlaintkList();
      storeTracComlaintkList();
    } catch (error) {
      print('Error fetching data: $error');
    }
  }

  Future<void> checkConnectivity() async {
    var connectivityResult = await (Connectivity().checkConnectivity());

    if (connectivityResult == ConnectivityResult.none) {
      print("No internet connection");

      setState(() {
        errorLod = true;
      });
    } else if (connectivityResult == ConnectivityResult.mobile) {
      print("Mobile data connection available");
      setState(() {
        errorLod = false;
      });
    } else if (connectivityResult == ConnectivityResult.wifi) {
      setState(() {
        errorLod = false;
      });
      print("WiFi connection available");
    }
  }

  // Function to retrieve status from SharedPreferences and populate the list
  Future<void> getDashboardChatFromSharedPreferences() async {
    try {
      final SharedPreferences prefs = await SharedPreferences.getInstance();
      final String? dashboardChatDataSerialzed =
          prefs.getString('dashboardChatModel');

      if (dashboardChatDataSerialzed != null &&
          dashboardChatDataSerialzed.isNotEmpty) {
        final List<dynamic> dataArray = jsonDecode(dashboardChatDataSerialzed);

        dashboardChatModel =
            dataArray.map((json) => DataItem.fromJson(json)).toList();

        // Update the lists if needed

        List<DataItem> updatedDashboardList = [];

        dashboardChatModel.forEach((status) {
          updatedDashboardList.add(status);
        });

        setState(() {
          allDashboardData = updatedDashboardList; // Update the status list
        });
      } else {
        print('No Dashboard data found in SharedPreferences.');
      }
    } catch (e) {
      print('Error retrieving Dashboard data from SharedPreferences: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    double scWidth = MediaQuery.of(context).size.width;
    double scHeight = MediaQuery.of(context).size.height;

    int len = allDashboardData.length;

    //  Pie Chat Data

    for (int i = 0; i < len; i++) {
      if (allDashboardData[i].code == "Total") {
        statuses1Name = allDashboardData[i].name;
        statuses1Colour = appcolorHex;
        statuses1Count = allDashboardData[i].total;
      } else if (allDashboardData[i].code ==
          "system_status_complaints_resolved") {
        statuses2Name = allDashboardData[i].name;
        statuses2Colour = allDashboardData[i].color;
        statuses2Count = allDashboardData[i].total;
      } else if (allDashboardData[i].code ==
          "system_status_complaints_in_process") {
        statuses3Name = allDashboardData[i].name;
        statuses3Colour = allDashboardData[i].color;
        statuses3Count = allDashboardData[i].total;
      } else if (allDashboardData[i].code ==
          "system_status_complaints_Reopened") {
        statuses4Name = allDashboardData[i].name;
        statuses4Colour = allDashboardData[i].color;
        statuses4Count = allDashboardData[i].total;
      }
    }

    // bool internetConnected = unter();

    return RefreshIndicator(
      onRefresh: refresh,
      child: Container(
        color: greyColor, // Set the background color of the container
        padding: EdgeInsets.only(
            left: marginLR + 20,
            right: marginLR + 20,
            top: scHeight / 80,
            bottom: scHeight / 80),
        child: SingleChildScrollView(
          child: Column(
            // crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Column(
                    mainAxisAlignment: MainAxisAlignment.start,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Container(
                        margin: EdgeInsets.only(bottom: 0),
                        child: Text(
                          "Hello,",
                          style: TextStyle(
                              fontSize: 20,
                              fontWeight: FontWeight.w500,
                              color: appcolor),
                        ),
                      ),
                      Container(
                        margin: EdgeInsets.only(bottom: 20),
                        child: Text(
                          "$userName",
                          style: TextStyle(
                              fontSize: 25,
                              fontWeight: FontWeight.w600,
                              color: dfGreyColor),
                        ),
                      ),
                    ],
                  ),
                  // isInternetConnect() == false
                  if (errorLod == true)
                    GestureDetector(
                      onTap: () {
                        AwesomeDialog(
                          context: context,
                          dialogType: DialogType.info,
                          animType: AnimType.bottomSlide,
                          title: 'No Internet Connection',
                          desc:
                              'No active internet connection was found! \n The app will now run in offline mode, for best experience, please connect to the internet!',
                          btnCancel: IconButton(
                            onPressed: () {
                              checkConnectivity();
                              Navigator.pop(context); // Close the dialog
                            },
                            icon: Image.asset(
                              'asserts/icons/checked.png',
                              width: 40,
                            ),
                            color: Colors.green,
                          ),
                        ).show();
                      },
                      child: Icon(
                        Icons.warning,
                        color: Colors.red,
                        size: scWidth / 12,
                      ),
                    )
                  else
                    Container(),

                  // IconButton(
                  //   onPressed: () {
                  //     print("Loading");
                  //     setState(() {
                  //       isLoading = true;
                  //       refresh();
                  //     });
                  //   },
                  //   icon: isLoading == true
                  //       ? Center(child: CircularProgressIndicator())
                  //       : Icon(
                  //           Icons.circle_outlined,
                  //           color: appcolor,
                  //           size: scWidth / 12,
                  //         ),
                  // ),
                ],
              ),
              isLoading
                  ? buildShimmer()
                  :
                  // print(allDashboardData);
                  Column(
                      children: [
                        Container(
                          padding: EdgeInsets.all(23),
                          decoration: const BoxDecoration(
                            shape: BoxShape.circle,
                            boxShadow: [
                              BoxShadow(
                                color: Color.fromARGB(
                                    31, 113, 180, 251), // Darker shadow color
                                blurRadius:
                                    15.0, // Adjust the spread of the shadow
                                offset:
                                    Offset(10, 16), // Adjust the shadow offset
                              ),
                              BoxShadow(
                                color: dfColor, // Background color
                                spreadRadius:
                                    -10.0, // Adjust the spread of the background color
                                blurRadius:
                                    1.0, // Adjust the blur of the background color
                              ),
                            ],
                          ),
                          child: Container(
                            margin:
                                EdgeInsets.symmetric(vertical: scHeight / 150),
                            child: Stack(
                              alignment: Alignment.center,
                              children: [
                                MyPieChart(
                                    colorinProcess:
                                        statuses3Colour ?? appcolorHex,
                                    colorresolved:
                                        statuses2Colour ?? appcolorHex,
                                    colorreOpen: statuses4Colour ?? appcolorHex,
                                    colortotal: appcolorHex,
                                    total: statuses1Count ?? 62,
                                    closed: 0,
                                    resolved: statuses2Count ?? 12,
                                    inProcess: statuses3Count ?? 13,
                                    reOpen: statuses4Count ?? 45),
                                GestureDetector(
                                  onTap: () {
                                    Get.offAll(() => OtherComplaints(),
                                        arguments: [
                                          allDashboardData[0].name ?? '.....',
                                          0
                                        ] // Pass your text data as an argument
                                        );
                                  },
                                  child: Center(
                                    child: Container(
                                        margin:
                                            EdgeInsets.only(bottom: 0, top: 0),
                                        child: Column(
                                          mainAxisAlignment:
                                              MainAxisAlignment.center,
                                          children: [
                                            Text(
                                              statuses1Count.toString(),
                                              textAlign: TextAlign.center,
                                              style: TextStyle(
                                                  fontSize: lgFontSize + 30,
                                                  fontWeight: FontWeight.w700,
                                                  color: appcolor),
                                            ),
                                            Text(
                                              // textAlign: TextAlign.center,

                                              "Total Complaints",
                                              textAlign: TextAlign.center,
                                              style: TextStyle(
                                                  fontSize: dfFontSize,
                                                  fontWeight: FontWeight.w500,
                                                  color: dfGreyColor),
                                            ),
                                          ],
                                        )),
                                  ),
                                )
                              ],
                            ),
                          ),
                        ),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            GestureDetector(
                              onTap: () {
                                Get.offAll(() => OtherComplaints(), arguments: [
                                  allDashboardData[0].name ?? '.....',
                                  0
                                ] // Pass your text data as an argument
                                    );
                              },
                              child: SizedBox(
                                width: scWidth / 2.5,
                                child: Card(
                                  margin: EdgeInsets.only(
                                      right: 15,
                                      top: scHeight / 60,
                                      bottom: 10),
                                  shape: RoundedRectangleBorder(
                                      borderRadius:
                                          BorderRadius.circular(12.0)),

                                  elevation:
                                      0, // Set elevation for a shadow effect

                                  color: dfColor, // Set background color
                                  child: Padding(
                                    padding: const EdgeInsets.symmetric(
                                        vertical: 5.0, horizontal: 17),
                                    child: Row(
                                      children: [
                                        // left side with an icon

                                        Container(
                                          alignment: Alignment.center,
                                          padding: EdgeInsets.all(7),
                                          decoration: BoxDecoration(
                                            color: appcolor,
                                            // Set the background color of the container
                                            borderRadius: BorderRadius.circular(
                                                360.0), // Set border radius
                                          ),

                                          child: Image.asset(
                                            'asserts/gifs/total.gif',
                                            width: 20,
                                            height: 20,
                                            // color: appcolor,
                                          ),
                                          //  Icon(Icons.incomplete_circle_outlined,
                                          //     size: scWidth / 20, color: dfColor),
                                        ),

                                        Spacer(), // Add space between text fields and icon
                                        // Left side with two text fields
                                        Column(
                                          children: [
                                            Text(
                                              textAlign: TextAlign.center,
                                              statuses1Count.toString(),
                                              style: TextStyle(
                                                  fontWeight: FontWeight.bold,
                                                  fontSize: scWidth / 20,
                                                  color: appcolor),
                                            ),
                                            SizedBox(
                                                height: 2), // Add some spacing
                                            Text(
                                              textAlign: TextAlign.center,
                                              '' +
                                                      statuses1Name.toString() +
                                                      '         ' ??
                                                  '.....',
                                              style: TextStyle(
                                                  fontSize: scWidth / 30,
                                                  fontWeight: FontWeight.w400,
                                                  color: Colors.black),
                                            ),
                                          ],
                                        ),
                                      ],
                                    ),
                                  ),
                                ),
                              ),
                            ),
                            GestureDetector(
                              onTap: () {
                                Get.offAll(() => OtherComplaints(), arguments: [
                                  allDashboardData[1].name ?? '.....',
                                  1
                                ] // Pass your text data as an argument
                                    );
                              },
                              child: Container(
                                width: scWidth / 2.5,
                                child: Card(
                                  margin: EdgeInsets.only(
                                      left: 15, top: scHeight / 60, bottom: 10),
                                  shape: RoundedRectangleBorder(
                                      borderRadius:
                                          BorderRadius.circular(12.0)),

                                  elevation:
                                      0, // Set elevation for a shadow effect

                                  color: dfColor, // Set background color
                                  child: Padding(
                                    padding: const EdgeInsets.symmetric(
                                        vertical: 5.0, horizontal: 17),
                                    child: Row(
                                      children: [
                                        // left side with an icon
                                        Container(
                                          padding: EdgeInsets.all(0),
                                          decoration: BoxDecoration(
                                            color: HexColor.fromHex(
                                                statuses2Colour ?? appcolorHex),
                                            // Set the background color of the container
                                            borderRadius: BorderRadius.circular(
                                                360.0), // Set border radius
                                          ),
                                          child: Image.asset(
                                            'asserts/gifs/resolved.gif',
                                            width: 35,
                                            height: 35,
                                            color: Colors.white,
                                          ),

                                          //  Icon(Icons.close_outlined,
                                          //     size: scWidth / 20, color: dfColor)
                                        ),

                                        Spacer(), // Add space between text fields and icon
                                        // Left side with two text fields
                                        Column(
                                          crossAxisAlignment:
                                              CrossAxisAlignment.center,
                                          children: [
                                            Text(
                                              textAlign: TextAlign.center,
                                              statuses2Count.toString(),
                                              style: TextStyle(
                                                  fontWeight: FontWeight.bold,
                                                  fontSize: scWidth / 20,
                                                  color: appcolor),
                                            ),
                                            SizedBox(
                                                height: 2), // Add some spacing
                                            Text(
                                              textAlign: TextAlign.center,
                                              statuses2Name ?? '....',
                                              // 'In Process',
                                              style: TextStyle(
                                                  fontSize: scWidth / 30,
                                                  fontWeight: FontWeight.w400,
                                                  color: Colors.black),
                                            ),
                                          ],
                                        ),
                                      ],
                                    ),
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            GestureDetector(
                              onTap: () {
                                Get.offAll(() => OtherComplaints(), arguments: [
                                  allDashboardData[2].name ?? '.....',
                                  2
                                ] // Pass your text data as an argument
                                    );
                              },
                              child: Container(
                                alignment: Alignment.center,
                                width: scWidth / 2.5,
                                child: Card(
                                  margin: EdgeInsets.only(
                                      right: 15,
                                      top: scHeight / 60,
                                      bottom: 10),
                                  shape: RoundedRectangleBorder(
                                      borderRadius:
                                          BorderRadius.circular(12.0)),
                                  elevation:
                                      0, // Set elevation for a shadow effect

                                  color: dfColor, // Set background color
                                  child: Padding(
                                    padding: const EdgeInsets.symmetric(
                                        vertical: 5.0, horizontal: 17),
                                    child: Row(
                                      children: [
                                        // left side with an icon
                                        Container(
                                            padding: EdgeInsets.all(0),
                                            decoration: BoxDecoration(
                                              color: HexColor.fromHex(
                                                  statuses3Colour ??
                                                      appcolorHex),
                                              // Set the background color of the container
                                              borderRadius: BorderRadius.circular(
                                                  360.0), // Set border radius
                                            ),
                                            child: Image.asset(
                                              'asserts/gifs/inproces.gif',
                                              width: 35,
                                              height: 35,
                                              // color: appcolor,
                                            )

                                            //  Icon(Icons.file_download_done_outlined,
                                            //     size: scWidth / 20, color: dfColor)
                                            ),

                                        Spacer(), // Add space between text fields and icon
                                        // Left side with two text fields
                                        Column(
                                          crossAxisAlignment:
                                              CrossAxisAlignment.center,
                                          children: [
                                            Text(
                                              textAlign: TextAlign.center,
                                              statuses3Count.toString(),
                                              // resolved.toString(),
                                              style: TextStyle(
                                                  fontWeight: FontWeight.bold,
                                                  fontSize: scWidth / 20,
                                                  color: appcolor),
                                            ),
                                            SizedBox(
                                                height: 2), // Add some spacing
                                            Text(
                                              textAlign: TextAlign.center,
                                              statuses3Name ?? '....',
                                              // 'Resolved',
                                              style: TextStyle(
                                                  fontSize: scWidth / 30,
                                                  fontWeight: FontWeight.w400,
                                                  color: Colors.black),
                                            ),
                                          ],
                                        ),
                                      ],
                                    ),
                                  ),
                                ),
                              ),
                            ),
                            GestureDetector(
                              onTap: () {
                                Get.offAll(() => OtherComplaints(), arguments: [
                                  allDashboardData[3].name ?? '.....',
                                  3
                                ] // Pass your text data as an argument
                                    );
                              },
                              child: Container(
                                width: scWidth / 2.5,
                                child: Card(
                                  margin: EdgeInsets.only(
                                      left: 15, top: scHeight / 60, bottom: 10),
                                  shape: RoundedRectangleBorder(
                                      borderRadius:
                                          BorderRadius.circular(12.0)),

                                  elevation:
                                      0, // Set elevation for a shadow effect

                                  color: dfColor, // Set background color
                                  child: Padding(
                                    padding: const EdgeInsets.symmetric(
                                        vertical: 5.0, horizontal: 17),
                                    child: Row(
                                      children: [
                                        // left side with an icon
                                        Container(
                                            padding: EdgeInsets.all(0),
                                            decoration: BoxDecoration(
                                              color: HexColor.fromHex(
                                                  statuses4Colour ??
                                                      appcolorHex),
                                              // Set the background color of the container
                                              borderRadius: BorderRadius.circular(
                                                  360.0), // Set border radius
                                            ),
                                            child: Image.asset(
                                              'asserts/gifs/reopen.gif',
                                              width: 35,
                                              height: 35,
                                              // color: appcolor,
                                            )

                                            // child: Icon(Icons.replay_outlined,
                                            //     size: scWidth / 20, color: dfColor),
                                            ),

                                        Spacer(), // Add space between text fields and icon
                                        // Left side with two text fields
                                        Column(
                                          crossAxisAlignment:
                                              CrossAxisAlignment.center,
                                          children: [
                                            Text(
                                              textAlign: TextAlign.center,
                                              statuses4Count.toString(),
                                              style: TextStyle(
                                                  fontWeight: FontWeight.bold,
                                                  fontSize: scWidth / 20,
                                                  color: appcolor),
                                            ),
                                            SizedBox(
                                                height: 2), // Add some spacing
                                            Text(
                                              textAlign: TextAlign.center,
                                              statuses4Name ?? '.....',
                                              // 'Re Open',
                                              style: TextStyle(
                                                  fontSize: scWidth / 30,
                                                  fontWeight: FontWeight.w400,
                                                  color: Colors.black),
                                            ),
                                          ],
                                        ),
                                      ],
                                    ),
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),

              //--------------

              permissions.contains('add_complaint')
                  ? Container(
                      margin: EdgeInsets.only(top: scHeight / 60),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          GestureDetector(
                            onTap: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                    builder: (context) => AddAreaSelection()),
                              );

                              // _showTwoSelectionDialog(context);
                            },
                            child: Container(
                              // width: scWidth / 2.6,
                              // height: scWidth / 4,
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                // mainAxisSize: MainAxisSize.min,
                                children: [
                                  Image.asset(
                                    'asserts/gifs/add.gif',
                                    width: scWidth / 3,
                                    // width: 120,
                                    // height: 120,
                                    // color: appcolor,
                                  ),
                                  // Change the color of the GIF
                                  // ColorFiltered(
                                  //   colorFilter: ColorFilter.mode(
                                  //     applightcolor, // Change the color here
                                  //     BlendMode.modulate,
                                  //   ),
                                  //   child: Image.asset(
                                  //     'asserts/gifs/add.gif',
                                  //     width: 120,
                                  //     height: 120,
                                  //   ),
                                  // ),
                                  // Image.asset(
                                  //   'asserts/gifs/add.gif',
                                  //   width: scWidth / 4,
                                  //   height: scHeight / 7.5,
                                  //   fit: BoxFit.cover,
                                  // ),
                                  // Icon(
                                  //   Icons.add,
                                  //   size: AppSize.s60,
                                  //   color: dfColor,
                                  // ),
                                ],
                              ),
                            ),
                          ),
                        ],
                      ),
                    )
                  : Container(
                      margin: EdgeInsets.only(top: scHeight / 75),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          GestureDetector(
                            onTap: () {
                              // Navigator.push(
                              //   context,
                              //   MaterialPageRoute(
                              //       builder: (context) => AddAreaSelection()),
                              // );
                              funToast(
                                  'You are not authorized to add a Complaint',
                                  Colors.red);

                              // _showTwoSelectionDialog(context);
                            },
                            child: Container(
                              // width: scWidth / 2.6,
                              // height: scWidth / 4,
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                // mainAxisSize: MainAxisSize.min,
                                children: [
                                  Container(
                                    margin: EdgeInsets.only(top: 25),
                                    padding: EdgeInsets.all(18),
                                    decoration: BoxDecoration(
                                        color: lightappcolor,
                                        shape: BoxShape.circle),
                                    child: Icon(
                                      Icons.add,
                                      size: 60,
                                      //  width: scWidth / 3,
                                      // width: 120,
                                      // height: 120,
                                      color: Colors.white,
                                    ),
                                  ),
                                  // Change the color of the GIF
                                  // ColorFiltered(
                                  //   colorFilter: ColorFilter.mode(
                                  //     applightcolor, // Change the color here
                                  //     BlendMode.modulate,
                                  //   ),
                                  //   child: Image.asset(
                                  //     'asserts/gifs/add.gif',
                                  //     width: 120,
                                  //     height: 120,
                                  //   ),
                                  // ),
                                  // Image.asset(
                                  //   'asserts/gifs/add.gif',
                                  //   width: scWidth / 4,
                                  //   height: scHeight / 7.5,
                                  //   fit: BoxFit.cover,
                                  // ),
                                  // Icon(
                                  //   Icons.add,
                                  //   size: AppSize.s60,
                                  //   color: dfColor,
                                  // ),
                                ],
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
            ],
          ),
        ),
      ),
    );
  }
}

Widget buildShimmer() {
  return Shimmer.fromColors(
    baseColor: Colors.grey[300]!,
    highlightColor: Colors.grey[100]!,
    child: ShimmerWidget(), // Customize this widget according to your UI
  );
}

class ShimmerWidget extends StatelessWidget {
  // Customize the shimmer effect according to your UI
  @override
  Widget build(BuildContext context) {
    double scWidth = MediaQuery.of(context).size.width;
    double scHeight = MediaQuery.of(context).size.height;
    return Column(
      children: [
        Container(
          padding: EdgeInsets.all(23),
          decoration: const BoxDecoration(
            shape: BoxShape.circle,
            boxShadow: [
              BoxShadow(
                color: Color.fromARGB(31, 113, 180, 251), // Darker shadow color
                blurRadius: 15.0, // Adjust the spread of the shadow
                offset: Offset(10, 16), // Adjust the shadow offset
              ),
              BoxShadow(
                color: dfColor, // Background color
                spreadRadius:
                    -10.0, // Adjust the spread of the background color
                blurRadius: 1.0, // Adjust the blur of the background color
              ),
            ],
          ),
          child: Container(
            margin: EdgeInsets.symmetric(vertical: 10),
            child: Stack(
              alignment: Alignment.center,
              children: [
                Container(
                  margin: EdgeInsets.all(marginLR - 5),
                  width: scWidth / 1.7, // Adjust the width as needed
                  height: scHeight / 3.4, // Adjust the height as needed
                  decoration: BoxDecoration(
                    color: Colors.blue, // Set your desired background color
                    borderRadius:
                        BorderRadius.circular(180), // Adjust the border radius
                    boxShadow: [
                      BoxShadow(
                        color: Colors.grey.withOpacity(0.5),
                        spreadRadius: 5,
                        blurRadius: 7,
                        offset: Offset(0, 3),
                      ),
                    ],
                  ),
                )
              ],
            ),
          ),
        ),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            SizedBox(
              width: scWidth / 2.5,
              height: scWidth / 5,
              child: Card(
                margin: EdgeInsets.only(right: 15, top: 10, bottom: 10),
                shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12.0)),

                elevation: 0, // Set elevation for a shadow effect

                color: dfColor, // Set background color
                child: Padding(
                  padding:
                      const EdgeInsets.symmetric(vertical: 5.0, horizontal: 17),
                  child: Row(
                    children: [
                      // left side with an icon

                      Container(
                        //  alignment: Alignment.center,
                        padding: EdgeInsets.all(7),
                        decoration: BoxDecoration(
                          color: appcolor,
                          // Set the background color of the container
                          borderRadius:
                              BorderRadius.circular(360.0), // Set border radius
                        ),

                        child: Image.asset(
                          'asserts/gifs/total.gif',
                          width: 20,
                          height: 20,
                          // color: appcolor,
                        ),
                        //  Icon(Icons.incomplete_circle_outlined,
                        //     size: scWidth / 20, color: dfColor),
                      ),

                      Spacer(), // Add space between text fields and icon
                      // Left side with two text fields
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          Text(
                            textAlign: TextAlign.center,
                            '.....',
                            style: TextStyle(
                                fontWeight: FontWeight.bold,
                                fontSize: scWidth / 20,
                                color: appcolor),
                          ),
                          SizedBox(height: 2), // Add some spacing
                          Text(
                            textAlign: TextAlign.center,
                            '.....',
                            style: TextStyle(
                                fontSize: scWidth / 30,
                                fontWeight: FontWeight.w400,
                                color: Colors.black),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
            ),
            Container(
              width: scWidth / 2.5,
              height: scWidth / 5,
              child: Card(
                margin: EdgeInsets.only(left: 15, top: 10, bottom: 10),
                shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12.0)),

                elevation: .0, // Set elevation for a shadow effect

                color: dfColor, // Set background color
                child: Padding(
                  padding:
                      const EdgeInsets.symmetric(vertical: 5.0, horizontal: 17),
                  child: Row(
                    children: [
                      // left side with an icon
                      Container(
                        padding: EdgeInsets.all(0),
                        decoration: BoxDecoration(
                          color: HexColor.fromHex(appcolorHex),
                          // Set the background color of the container
                          borderRadius:
                              BorderRadius.circular(360.0), // Set border radius
                        ),
                        child: Image.asset(
                          'asserts/gifs/resolved.gif',
                          width: 35,
                          height: 35,
                          color: Colors.white,
                        ),

                        //  Icon(Icons.close_outlined,
                        //     size: scWidth / 20, color: dfColor)
                      ),

                      Spacer(), // Add space between text fields and icon
                      // Left side with two text fields
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          Text(
                            textAlign: TextAlign.center,
                            '.....',
                            style: TextStyle(
                                fontWeight: FontWeight.bold,
                                fontSize: scWidth / 20,
                                color: appcolor),
                          ),
                          SizedBox(height: 2), // Add some spacing
                          Text(
                            textAlign: TextAlign.center,
                            '.....',
                            // 'In Process',
                            style: TextStyle(
                                fontSize: scWidth / 30,
                                fontWeight: FontWeight.w400,
                                color: Colors.black),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Container(
              width: scWidth / 2.5,
              height: scWidth / 5,
              child: Card(
                margin: EdgeInsets.only(right: 15, top: 10, bottom: 10),
                shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12.0)),
                elevation: 0, // Set elevation for a shadow effect

                color: dfColor, // Set background color
                child: Padding(
                  padding:
                      const EdgeInsets.symmetric(vertical: 5.0, horizontal: 17),
                  child: Row(
                    children: [
                      // left side with an icon
                      Container(
                          padding: EdgeInsets.all(0),
                          decoration: BoxDecoration(
                            color: HexColor.fromHex(appcolorHex),
                            // Set the background color of the container
                            borderRadius: BorderRadius.circular(
                                360.0), // Set border radius
                          ),
                          child: Image.asset(
                            'asserts/gifs/inproces.gif',
                            width: 35,
                            height: 35,
                            // color: appcolor,
                          )

                          //  Icon(Icons.file_download_done_outlined,
                          //     size: scWidth / 20, color: dfColor)
                          ),

                      Spacer(), // Add space between text fields and icon
                      // Left side with two text fields
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          Text(
                            textAlign: TextAlign.center,
                            '.....',
                            // resolved.toString(),
                            style: TextStyle(
                                fontWeight: FontWeight.bold,
                                fontSize: scWidth / 20,
                                color: appcolor),
                          ),
                          SizedBox(height: 2), // Add some spacing
                          Text(
                            textAlign: TextAlign.center,
                            '.....',
                            // 'Resolved',
                            style: TextStyle(
                                fontSize: scWidth / 30,
                                fontWeight: FontWeight.w400,
                                color: Colors.black),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
            ),
            Container(
              width: scWidth / 2.5,
              height: scWidth / 5,
              child: Card(
                margin: EdgeInsets.only(left: 15, top: 10, bottom: 10),
                shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12.0)),

                elevation: 0, // Set elevation for a shadow effect

                color: dfColor, // Set background color
                child: Padding(
                  padding:
                      const EdgeInsets.symmetric(vertical: 5.0, horizontal: 17),
                  child: Row(
                    children: [
                      // left side with an icon
                      Container(
                          padding: EdgeInsets.all(0),
                          decoration: BoxDecoration(
                            color: HexColor.fromHex(appcolorHex),
                            // Set the background color of the container
                            borderRadius: BorderRadius.circular(
                                360.0), // Set border radius
                          ),
                          child: Image.asset(
                            'asserts/gifs/reopen.gif',
                            width: 35,
                            height: 35,
                            // color: appcolor,
                          )

                          // child: Icon(Icons.replay_outlined,
                          //     size: scWidth / 20, color: dfColor),
                          ),

                      Spacer(), // Add space between text fields and icon
                      // Left side with two text fields
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          Text(
                            textAlign: TextAlign.center,
                            '.....',
                            style: TextStyle(
                                fontWeight: FontWeight.bold,
                                fontSize: scWidth / 20,
                                color: appcolor),
                          ),
                          SizedBox(height: 2), // Add some spacing
                          Text(
                            textAlign: TextAlign.center,
                            '.....',
                            // 'Re Open',
                            style: TextStyle(
                                fontSize: scWidth / 30,
                                fontWeight: FontWeight.w400,
                                color: Colors.black),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
      ],
    );
  }
}
