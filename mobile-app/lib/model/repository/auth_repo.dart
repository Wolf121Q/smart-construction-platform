import 'dart:async';
import 'package:dha_ctt_app/model/apis/api_client.dart';
import 'package:dha_ctt_app/model/resources/string_manager.dart';
import 'package:get/get.dart';

class AuthRepo {
  final ApiClient apiClient;
  AuthRepo({
    required this.apiClient,
  });

  Future<Response> login(String username, String password) async {
    return await apiClient.postData(
        AppStrings.LOGIN_URI, {"username": username, "password": password});
  }

  Future<Response> dashboard() async {
    return await apiClient.getData(
      AppStrings.DASHBOARD_CHART_DATA,
    );
  }
}
