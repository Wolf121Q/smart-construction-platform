import 'dart:async';
import 'dart:convert';
import 'package:dha_ctt_app/model/apis/api_client.dart';
import 'package:dha_ctt_app/model/database/local_db.dart';
import 'package:dha_ctt_app/model/repository/auth_repo.dart';
import 'package:dha_ctt_app/model/shared_preferences/share_pref_api_function.dart';
import 'package:dha_ctt_app/view/screens/dashboard/home.dart';
import 'package:dha_ctt_app/view_model/view_models/dashboard_model/dashboard_chat_model.dart';
import 'package:flutter/material.dart';
import 'package:get_storage/get_storage.dart';
import 'package:package_info/package_info.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:shimmer/shimmer.dart';
import 'package:upgrader/upgrader.dart';

import '../../../constant.dart';
import '../login/login.dart';

class Splach extends StatefulWidget {
  const Splach({super.key});

  @override
  State<Splach> createState() => _SplachState();
}

class _SplachState extends State<Splach> {
  Timer? _timer;
  List<DataItem> dashboardChatModel = [];
  List<DataItem> allDashboardData = [];
  static String appVersion = 'Version 2.0.4';
  var box = GetStorage();
  final AuthRepo authRepo = AuthRepo(apiClient: ApiClient());
  _startDelay() {
    _timer = Timer(Duration(seconds: 3), _goNext);
  }

  checkVersion() async {
    PackageInfo packageInfo = await PackageInfo.fromPlatform();
    appVersion = 'Version ' + packageInfo.version.toString();
  }

  _goNext() async {
    String userEmail = await DBManager().fetchLoginUserEmail();

    if (userEmail != "") {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
            builder: (context) => UpgradeAlert(
                  upgrader: Upgrader(
                    showIgnore: false,
                    showLater: false,
                    showReleaseNotes: false,
                    canDismissDialog: false,
                    durationUntilAlertAgain: const Duration(microseconds: 1),
                  ),
                  child: Home(
                    arguments2: 'splach',
                  ),
                )),
      );

      // Get.offAll(

      //   () => Home(),
      //   arguments: 'splach',
      // );
    } else {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
            builder: (context) => UpgradeAlert(
                upgrader: Upgrader(
                  showIgnore: false,
                  showLater: false,
                  showReleaseNotes: false,
                  canDismissDialog: false,
                  durationUntilAlertAgain: const Duration(microseconds: 1),
                ),
                child: LogIn())),
      );

      // Get.offAll(() => LogIn());
    }
  }

  @override
  void initState() {
    super.initState();
    // checkForUpdates();
    // Timer(const Duration(seconds: 5), () => checkSessionStatus());
    checkVersion();
    _startDelay();
    storeDashboardChartApi();

    storeCategorieslistApi();
    storeQACategorieslistApi();
    storeStatusApi();
    storeArealistApi(); // This will be logged
    storeOthersComlaintkList();
    storeTracComlaintkList();
    getDashboardChatFromSharedPreferences();
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  //----------------------
  // Function to retrieve status from SharedPreferences and populate the list

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

  // Future<void> getDashboardChatFromSharedPreferences(
  //     List<DataItem> dashboardChatModel,
  //     List<DataItem> allDashboardData) async {
  //   try {
  //     final SharedPreferences prefs = await SharedPreferences.getInstance();
  //     final String? dashboardChatDataSerialzed =
  //         prefs.getString('dashboardChatModel');

  //     if (dashboardChatDataSerialzed != null &&
  //         dashboardChatDataSerialzed.isNotEmpty) {
  //       final List<dynamic> dataArray = jsonDecode(dashboardChatDataSerialzed);

  //       dashboardChatModel =
  //           dataArray.map((json) => DataItem.fromJson(json)).toList();

  //       // Update the lists if needed

  //       List<DataItem> updatedDashboardList = [];

  //       dashboardChatModel.forEach((status) {
  //         updatedDashboardList.add(status);
  //       });

  //       setState(() {
  //         allDashboardData = updatedDashboardList; // Update the status list
  //       });
  //     } else {
  //       print('No Dashboard data found in SharedPreferences.');
  //     }
  //   } catch (e) {
  //     print('Error retrieving Dashboard data from SharedPreferences: $e');
  //   }
  // }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
          // Adjust the height as needed
          color: appcolor, // Container background color
          child: Container(
            margin: EdgeInsets.symmetric(vertical: marginLR),
            alignment: Alignment.center,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Stack(
                  alignment: Alignment.center,
                  children: [
                    Image.asset(
                      'asserts/icons/app_icon.png', // Replace with your actual asset path
                      width: 150,
                      height: 150,
                    ),
                    Shimmer.fromColors(
                      period: Duration(milliseconds: 1500),
                      baseColor: Colors.transparent,
                      highlightColor: Colors.white70,
                      child: Container(
                        alignment: Alignment.center,
                        width: 120,
                        height: 120,
                        decoration: BoxDecoration(
                          borderRadius:
                              BorderRadius.circular(75), // Adjust as needed
                          color: Colors.white, // Adjust as needed
                        ),
                      ),
                    ),
                  ],
                ),
                Container(
                  margin: EdgeInsets.symmetric(vertical: 10),
                  child: Text(
                    appVersion.toString(),
                    style: TextStyle(
                        color: dfColor,
                        fontSize: exSmFontSize,
                        fontWeight: FontWeight.normal),
                  ),
                ),
                Text(
                  "Complaint Management System",
                  style: TextStyle(
                      color: dfColor,
                      fontSize: 18,
                      fontWeight: FontWeight.bold),
                ),
                Text(
                  "Company City",
                  style: TextStyle(
                    color: dfColor,
                    fontSize: 18,
                  ),
                ),
              ],
            ),
          )),
    );
  }
}
