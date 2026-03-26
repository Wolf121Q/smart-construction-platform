import 'dart:convert';

import 'package:dha_ctt_app/model/resources/string_manager.dart';
import 'package:dha_ctt_app/view/screens/dashboard/home.dart';
import 'package:dha_ctt_app/view/screens/login/login.dart';
import 'package:dha_ctt_app/view_model/view_models/dashboard_model/dashboard_chat_model.dart';
import 'package:dha_ctt_app/view_model/view_models/login_model/login_model.dart';
import 'package:flutter/foundation.dart';
import 'package:get/get.dart';
import 'package:get_storage/get_storage.dart';

class DBManager {
  var box = GetStorage();

  //  // save Login Data to Database
  Future<void> saveUserData(Response response) async {
    box.write(LocalDBStrings.login_user, jsonEncode(response.body));
  }

  //  // save Dashboard Data to Database
  Future<void> saveDashboardData(Response response) async {
    box.write(LocalDBStrings.dashboard_chart, jsonEncode(response.body));
  }

  //get Login data from database
  Future<String> fetchLoginUserEmail() async {
    var user = box.read(LocalDBStrings.login_user);
    String userEmail = "";
    if (user != null) {
      try {
        var decodedUser = jsonDecode(user);
        var _user = LogInModel.fromJson(decodedUser);
        userEmail = _user.email.toString();
      } catch (e) {
        debugPrint("catch:$e");
      }
    } else {
      Get.offAll(() => Home());
    }
    return userEmail;
  }

  Future<String> fetchLoginUserToken() async {
    var user = box.read(LocalDBStrings.login_user);
    String userToken = "";
    if (user != null) {
      try {
        var decodedUser = jsonDecode(user);
        var _user = LogInModel.fromJson(decodedUser);
        userToken = _user.accessToken.toString();
      } catch (e) {
        debugPrint("catch:$e");
      }
    } else {
      Get.offAll(() => Home());
    }
    return userToken;
  }

  Future<LogInModel> fetchLoginUser() async {
    var user = box.read(LocalDBStrings.login_user);
    String userEmail = "";
    String userToken = "";
    if (user != null) {
      try {
        var decodedUser = jsonDecode(user);
        var _user = LogInModel.fromJson(decodedUser);
        userEmail = _user.email.toString();
        userToken = _user.accessToken.toString();
      } catch (e) {
        debugPrint("catch:$e");
      }
    } else {
      Get.offAll(() => Home());
    }
    return user;
  }

//get Dashboard data from database
  Future<DashboardChatModel> fetchDashboardChart() async {
    DashboardChatModel dashboardChatModel = DashboardChatModel();
    var data = box.read(LocalDBStrings.dashboard_chart);

    try {
      if (data != null) {
        var decodedData = jsonDecode(data);
        print("DashBorad" + decodedData);
        dashboardChatModel = DashboardChatModel.fromJson(decodedData);
      } else {
        Get.offAll(() => LogIn());
      }
    } catch (e) {
      debugPrint("catch:$e");
    }

    return dashboardChatModel;
  }
}
