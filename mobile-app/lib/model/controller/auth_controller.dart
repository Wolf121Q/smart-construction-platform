import 'dart:convert';

import 'package:dha_ctt_app/model/apis/api_client.dart';
import 'package:dha_ctt_app/model/database/local_db.dart';
import 'package:dha_ctt_app/model/repository/auth_repo.dart';
import 'package:dha_ctt_app/model/response/response_model.dart';
import 'package:dha_ctt_app/model/shared_preferences/share_preferences_session.dart';
import 'package:dha_ctt_app/view/widgets/dialogs/alert_dialogs.dart';
import 'package:dha_ctt_app/view_model/view_models/dashboard_model/dashboard_chat_model.dart';
import 'package:dha_ctt_app/view_model/view_models/login_model/login_model.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class AuthController extends GetxController implements GetxService {
  final AuthRepo authRepo = AuthRepo(apiClient: ApiClient());
  bool isLoading = false;
  AuthController() {}

  @override
  void onInit() {
    super.onInit();
    // initDB();
  }

  Future<ResponseModel> login(String username, String password) async {
    isLoading = true;
    update();
    // Save login time
    final loginTimestamp = DateTime.now().millisecondsSinceEpoch;
    final loginDateTime = DateTime.fromMillisecondsSinceEpoch(loginTimestamp);
    final response = await authRepo.login(username, password);
    ResponseModel responseModel;

    if (response.statusCode == 200) {
      print("Response LogIn :" + response.body.toString());

      // final Map<String, dynamic> responseData = json.decode(response.body);

      final jsonResponse = LogInModel.fromJson(response.body);
      final status = jsonResponse.status;
      final longtoken = jsonResponse.accessToken;
      print(longtoken);

      if (status == 1) {
        await DBManager().saveUserData(response);
        String userEmail = await DBManager().fetchLoginUserEmail();

        final sessionData = {
          'status': jsonResponse.status,
          'message': jsonResponse.message,
          'access_token': jsonResponse.accessToken,
          'token_expiry_time': jsonResponse.tokenExpiryTime,
          'user_area_type_id': jsonResponse.userAreaTypeId,
          'username': jsonResponse.username,
          'email': jsonResponse.email,
          'permissions': jsonResponse.permissions,
          'login_time': loginTimestamp,
        };

        // final sessionData = {
        //   'status': jsonResponse.status,
        //   'message': jsonResponse.message,
        //   'access_token': jsonResponse.accessToken,
        //   'user_area_type_id': jsonResponse.userAreaTypeId,
        //   'username': jsonResponse.username,
        //   'email': jsonResponse.email,
        //   'login_time': loginTimestamp,
        // };
        saveSessionData(sessionData);
        funToast(jsonResponse.message, Colors.green);

        print("Login time $loginTimestamp");
        print("session data saved!");
        print("Hello $userEmail");
        responseModel = ResponseModel(true, response.body['message']);
      } else {
        responseModel = ResponseModel(false, response.body['message']);
      }
    } else {
      print('Unexpected response status code: ${response.statusCode}');
      print('Response body: ${response.body}');

      responseModel = ResponseModel(false, response.statusText.toString());
    }
    isLoading = false;
    update();
    return responseModel;
  }

  Future<DashboardChatModel> dashboardChart() async {
    isLoading = true;
    update();

    Response response = await authRepo.dashboard();
    ResponseModel responseModel;

    if (response.statusCode == 200) {
      print("Response Dashboad :" + response.body.toString());

      final Map<String, dynamic> responseData = json.decode(response.body);

      final jsonResponse = DashboardChatModel.fromJson(responseData);
      final status = jsonResponse.status;

      print("$jsonResponse");

      if (status == 1) {
        // await DBManager().saveDashboardData(jsonResponse);
        // String userEmail = await DBManager().fetchLoginUserEmail();

        final sessionData = {
          'status': jsonResponse.status,
          'message': jsonResponse.message,
          'data': jsonResponse.data,
        };
        print(jsonResponse.status);
        print(jsonResponse.message);
        print(jsonResponse.data);

        // funToast(jsonResponse.message!, Colors.green);

        // print("session data saved!");
        responseModel = ResponseModel(true, response.body['message']);
      } else {
        responseModel = ResponseModel(false, response.body['message']);
      }
      return DashboardChatModel.fromJson(responseData);
    } else {
      print('Unexpected response status code: ${response.statusCode}');
      print('Response body: ${response.body}');

      isLoading = false;
      update();

      responseModel = ResponseModel(false, response.statusText.toString());
      throw Exception("Failed to load data");
    }

    // return response;
  }

  Future<DashboardChatModel> fetchData() async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    final String token = prefs.getString('access_token') ?? '';

    Map<String, String> headers = {
      'Authorization': 'Bearer $token',
    };
    final response = await http.get(
        Uri.parse("http://58.65.172.155:54327/complaint/api/dashboard_api"),
        headers: headers);

    if (response.statusCode == 200) {
      final Map<String, dynamic> jsonData = json.decode(response.body);

      print("Status: " + jsonData['status'].toString());

      if (jsonData['status'] == 1) {}

      return DashboardChatModel.fromJson(jsonData);
    } else {
      throw Exception('Failed to load data');
    }
  }
}
