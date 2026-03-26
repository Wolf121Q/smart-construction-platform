import 'dart:convert';
import 'dart:io';
import 'package:awesome_dialog/awesome_dialog.dart';
import 'package:dha_ctt_app/model/shared_preferences/share_preferences_session.dart';
import 'package:dha_ctt_app/view/screens/login/login.dart';
import 'package:dha_ctt_app/view_model/utils/http_utils.dart';
import 'package:dha_ctt_app/view_model/view_models/complaint_state_model/complaint_action_comments.dart';
import 'package:dha_ctt_app/view_model/view_models/complaint_state_model/complaint_image_model.dart';
import 'package:dha_ctt_app/view_model/view_models/complaint_state_model/complaint_list_long_detail_model.dart';
import 'package:dha_ctt_app/view_model/view_models/complaint_state_model/other_complaint_list_model.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:get_storage/get_storage.dart';
import 'package:http/http.dart' as http;
import 'package:path_provider/path_provider.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:dha_ctt_app/model/resources/string_manager.dart';
import 'package:dha_ctt_app/view_model/view_models/dashboard_model/dashboard_chat_model.dart';
import 'package:dha_ctt_app/view_model/view_models/new_complaint_model/area_hierarchy.dart';
import 'package:dha_ctt_app/view_model/view_models/qa_checklist/qa_checklist_model.dart';
import 'package:dha_ctt_app/view_model/view_models/new_complaint_model/category_model.dart';
import 'package:dha_ctt_app/view_model/view_models/new_complaint_model/complaint_status_model.dart';
import 'package:dha_ctt_app/view_model/view_models/complaint_state_model/complaint_list_detail_model.dart';

String appBaseUrl = AppStrings.appBaseUrl;

//Dashboard chart
String appDashboard = AppStrings.DASHBOARD_CHART_DATA;

//Compaint Category
String appNewcomplaint = AppStrings.NEW_COMPLAINT;
String appGetCategory = AppStrings.GET_CATEGORY;

//QA Category
String appQAchecklist = AppStrings.QA_CHECKLIST;
String appGetQACategory = AppStrings.QA_GET_CATEGORY;

//Statuses
String appComplaintStatuses = AppStrings.COMPLAINT_STATUS;

//Statuses
String appUpdateComplaint = AppStrings.UPDATE_COMPLAINT_LIST;

//Area Hierarchy
String appAreaHierarchy = AppStrings.AREA_HIERARCHY;

//Track own Comlaints List
String trackComplaintList = AppStrings.OWN_COMPLAINT_LIST;

//Track others Comlaints List
String othersComplaintList = AppStrings.OTHER_COMPLAINT_LIST;

// Complaint Details
String complaintDetails = AppStrings.COMPLAINT_ACTION_LIST_DETAILS;
String complaintCommnentsDetails = AppStrings.COMPLAINT_ACTION_COMMENTS_DETAILS;
String complaintComnetsImageDetails =
    AppStrings.COMPLAINT_ACTION_COMMENTS_IMAGE_DETAILS;

//  Shared Pref Category
Future<void> storeCategorieslistApi() async {
  final SharedPreferences prefs = await SharedPreferences.getInstance();
  final String token = prefs.getString('access_token') ?? '';

  Map<String, String> headers = {
    'Authorization': 'Bearer $token',
  };

  final Uri requestUri = Uri.parse(appBaseUrl + appGetCategory);

  try {
    final response = await getRequest(requestUri, headers: headers);

    if (response.statusCode == 200) {
      final Map<String, dynamic> data = jsonDecode(response.body);
      final List<dynamic> dataArray = data['response_data'];
      final List<Item> chatagoriDataArray =
          dataArray.map((jsonData) => Item.fromJson(jsonData)).toList();

      // Convert Item instances to JSON-compatible maps
      final List<Map<String, dynamic>> serializedData = chatagoriDataArray
          .map((chatagoriItem) => chatagoriItem.toJson())
          .toList();

      // Store the serialized data in SharedPreferences
      await prefs.setString('chatagoriDataArray', jsonEncode(serializedData));

      print('Data successfully stored in SharedPreferences.');
    } else {
      print('API request failed with status: ${response.statusCode}.');
    }
  } catch (e) {
    print('Exception occurred: $e');
  }
}
// Future<void> storeCategorieslistApi() async {
//   final SharedPreferences prefs = await SharedPreferences.getInstance();
//   final String token = prefs.getString('access_token') ?? '';

//   Map<String, String> headers = {
//     'Authorization': 'Bearer $token',
//   };
//   final response =
//       await http.get(Uri.parse(appBaseUrl + appGetCategory), headers: headers);

//   // print("Step 1: ${response.body}");

//   if (response.statusCode == 200) {
//     final Map<String, dynamic> data = jsonDecode(response.body);
//     final List<dynamic> dataArray = data['response_data'];
//     final List<Item> chatagoriDataArray =
//         dataArray.map((jsonData) => Item.fromJson(jsonData)).toList();

//     // Convert Item instances to JSON-compatible maps
//     final List<Map<String, dynamic>> serializedData = chatagoriDataArray
//         .map((chatagoriItem) => chatagoriItem.toJson())
//         .toList();

//     // Store the serialized data in SharedPreferences
//     await prefs.setString('chatagoriDataArray', jsonEncode(serializedData));
//     //print(chatagoriDataArray);
//     // Now you have the chatagoriDataArray stored in SharedPreferences
//   } else {
//     print('API request failed with status: ${response.statusCode}.');
//   }
// }

//  Shared Pref QA Category

Future<void> storeQACategorieslistApi() async {
  final SharedPreferences prefs = await SharedPreferences.getInstance();
  final String token = prefs.getString('access_token') ?? '';

  Map<String, String> headers = {
    'Authorization': 'Bearer $token',
  };

  final Uri requestUri = Uri.parse(appBaseUrl + appGetQACategory);

  try {
    final response = await getRequest(requestUri, headers: headers);

    if (response.statusCode == 200) {
      final Map<String, dynamic> data = jsonDecode(response.body);
      final List<dynamic> dataArray = data['response_data'];
      final List<QAChecklistItem> chatagoriDataArray = dataArray
          .map((jsonData) => QAChecklistItem.fromJson(jsonData))
          .toList();

      // Convert QAChecklistItem instances to JSON-compatible maps
      final List<Map<String, dynamic>> serializedData = chatagoriDataArray
          .map((chatagoriItem) => chatagoriItem.toJson())
          .toList();

      // Store the serialized data in SharedPreferences
      await prefs.setString('qachatagoriDataArray', jsonEncode(serializedData));

      print('Data successfully stored in SharedPreferences.');
    } else {
      print('API request failed with status: ${response.statusCode}.');
    }
  } catch (e) {
    print('Exception occurred: $e');
  }
}

// Future<void> storeQACategorieslistApi() async {
//   final SharedPreferences prefs = await SharedPreferences.getInstance();
//   final String token = prefs.getString('access_token') ?? '';

//   Map<String, String> headers = {
//     'Authorization': 'Bearer $token',
//   };
//   final response = await http.get(Uri.parse(appBaseUrl + appGetQACategory),
//       headers: headers);

//   // print("Step 1: ${response.body}");

//   if (response.statusCode == 200) {
//     final Map<String, dynamic> data = jsonDecode(response.body);
//     final List<dynamic> dataArray = data['response_data'];
//     final List<QAChecklistItem> chatagoriDataArray = dataArray
//         .map((jsonData) => QAChecklistItem.fromJson(jsonData))
//         .toList();

//     // Convert QAChecklistItem instances to JSON-compatible maps
//     final List<Map<String, dynamic>> serializedData = chatagoriDataArray
//         .map((chatagoriItem) => chatagoriItem.toJson())
//         .toList();

//     // Store the serialized data in SharedPreferences
//     await prefs.setString('qachatagoriDataArray', jsonEncode(serializedData));
//     //print(chatagoriDataArray);
//     // Now you have the chatagoriDataArray stored in SharedPreferences
//   } else {
//     print('API request failed with status: ${response.statusCode}.');
//   }
// }

// Shared Pref category Statuses
Future<void> storeStatusApi() async {
  print('Initiating status API request...');

  final SharedPreferences prefs = await SharedPreferences.getInstance();
  final String token = prefs.getString('access_token') ?? '';

  Map<String, String> headers = {
    'Authorization': 'Bearer $token',
  };

  final Uri requestUri = Uri.parse(appBaseUrl + appComplaintStatuses);

  try {
    final response = await getRequest(requestUri, headers: headers);

    if (response.statusCode == 200) {
      print('Status API request successful.');

      final Map<String, dynamic> data = jsonDecode(response.body);
      final List<dynamic> dataArray = data['response_data'];
      final List<ComplaintStatusesModel> statusDataArray = dataArray
          .map((jsonData) => ComplaintStatusesModel.fromJson(jsonData))
          .toList();

      // Convert ComplaintStatusesModel instances to JSON-compatible maps
      final List<Map<String, dynamic>> serializedData =
          statusDataArray.map((statusItem) => statusItem.toJson()).toList();

      // Store the serialized data in SharedPreferences
      await prefs.setString('statusDataArray', jsonEncode(serializedData));
    } else {
      print('API request failed with status: ${response.statusCode}.');
    }
  } catch (e) {
    print('Exception occurred: $e');
  }
}
// Future<void> storeStatusApi() async {
//   final SharedPreferences prefs = await SharedPreferences.getInstance();
//   final String token = prefs.getString('access_token') ?? '';

//   Map<String, String> headers = {
//     'Authorization': 'Bearer $token',
//   };
//   final response = await http.get(Uri.parse(appBaseUrl + appComplaintStatuses),
//       headers: headers);

//   // print("Step 1: ${response.body}");

//   if (response.statusCode == 200) {
//     final Map<String, dynamic> data = jsonDecode(response.body);
//     final List<dynamic> dataArray = data['response_data'];
//     final List<ComplaintStatusesModel> chatagoriDataArray = dataArray
//         .map((jsonData) => ComplaintStatusesModel.fromJson(jsonData))
//         .toList();

//     // Convert Item instances to JSON-compatible maps
//     final List<Map<String, dynamic>> serializedData = chatagoriDataArray
//         .map((chatagoriItem) => chatagoriItem.toJson())
//         .toList();

//     // Store the serialized data in SharedPreferences
//     await prefs.setString('statusDataArray', jsonEncode(serializedData));
//     //print(chatagoriDataArray);
//     // Now you have the chatagoriDataArray stored in SharedPreferences
//   } else {
//     print('API request failed with status: ${response.statusCode}.');
//   }
// }

// Shared Pref Area Hierarchy

Future<void> storeArealistApi() async {
  final SharedPreferences prefs = await SharedPreferences.getInstance();
  final String token = prefs.getString('access_token') ?? '';

  Map<String, String> headers = {
    'Authorization': 'Bearer $token',
  };

  final Uri requestUri = Uri.parse(appBaseUrl + appAreaHierarchy);

  try {
    final response = await getRequest(requestUri, headers: headers);

    if (response.statusCode == 200) {
      final Map<String, dynamic> data = jsonDecode(response.body);
      final List<dynamic> dataArray = data['response_data'];
      final List<AreaHierarchy> chatagoriDataArray = dataArray
          .map((jsonData) => AreaHierarchy.fromJson(jsonData))
          .toList();

      // Convert AreaHierarchy instances to JSON-compatible maps
      final List<Map<String, dynamic>> serializedData = chatagoriDataArray
          .map((chatagoriItem) => chatagoriItem.toJson())
          .toList();

      // Store the serialized data in SharedPreferences
      await prefs.setString('areaHierarchy', jsonEncode(serializedData));

      print('Data successfully stored in SharedPreferences.');
    } else {
      print('API request failed with status: ${response.statusCode}.');
    }
  } catch (e) {
    print('Exception occurred: $e');
  }
}

// Future<void> storeArealistApi() async {
//   final SharedPreferences prefs = await SharedPreferences.getInstance();
//   final String token = prefs.getString('access_token') ?? '';

//   Map<String, String> headers = {
//     'Authorization': 'Bearer $token',
//   };
//   final response = await http.get(Uri.parse(appBaseUrl + appAreaHierarchy),
//       headers: headers);

//   if (response.statusCode == 200) {
//     final Map<String, dynamic> data = jsonDecode(response.body);
//     final List<dynamic> dataArray = data['response_data'];
//     final List<AreaHierarchy> chatagoriDataArray =
//         dataArray.map((jsonData) => AreaHierarchy.fromJson(jsonData)).toList();

//     // Convert AreaHierarchy instances to JSON-compatible maps
//     final List<Map<String, dynamic>> serializedData = chatagoriDataArray
//         .map((chatagoriItem) => chatagoriItem.toJson())
//         .toList();

//     // Store the serialized data in SharedPreferences
//     await prefs.setString('areaHierarchy', jsonEncode(serializedData));
//     //print(chatagoriDataArray);
//     // Now you have the chatagoriDataArray stored in SharedPreferences
//   } else {
//     print('API request failed with status: ${response.statusCode}.');
//   }
// }

//Shared Pref Dashboard
Future<void> storeDashboardChartApi() async {
  final SharedPreferences prefs = await SharedPreferences.getInstance();
  final String token = prefs.getString('access_token') ?? '';

  Map<String, String> headers = {
    'Authorization': 'Bearer $token',
  };

  final Uri requestUri = Uri.parse(appBaseUrl + appDashboard);

  print('Initiating Dashboard API request...');
  try {
    final response = await http.get(requestUri, headers: headers);

    print("Response : " + response.toString());

    if (response.statusCode == 200) {
      print('Dashboard API request successful.');

      final Map<String, dynamic> data = jsonDecode(response.body);
      final List<dynamic> dataArray = data['data'];

      // Convert DataItem instances to JSON-compatible maps
      final List<Map<String, dynamic>> serializedData = dataArray
          .map((jsonData) => DataItem.fromJson(jsonData).toJson())
          .toList();

      // Store the serialized data in SharedPreferences
      await prefs.setString('dashboardChatModel', jsonEncode(serializedData));

      print('Dashboard data stored in SharedPreferences.');
    } else {
      print('API request failed with status: ${response.statusCode}.');
    }
  } catch (e) {
    print('Exception occurred: $e');
  }
}

// Future<void> storeDashboardChartApi() async {
//   final SharedPreferences prefs = await SharedPreferences.getInstance();
//   final String token = prefs.getString('access_token') ?? '';

//   Map<String, String> headers = {
//     'Authorization': 'Bearer $token',
//   };
//   final response =
//       await http.get(Uri.parse(appBaseUrl + appDashboard), headers: headers);

//   print("Responce : " + response.toString());

//   if (response.statusCode == 200) {
//     // final jsonData = json.decode(response.body);
//     final Map<String, dynamic> data = jsonDecode(response.body);
//     final List<dynamic> dataArray = data['data'];

//     final List<DataItem> dashboardDataArray =
//         dataArray.map((jsonData) => DataItem.fromJson(jsonData)).toList();

//     final List<Map<String, dynamic>> serializedData = dashboardDataArray
//         .map((dashboardItem) => dashboardItem.toJson())
//         .toList();

//     print(serializedData);

//     //Save Dashboard data
//     // saveDashboardChatModelToPrefs(jsonData);
//     //

//     await prefs.setString('dashboardChatModel', jsonEncode(serializedData));
//   } else {
//     print("API request failed with status: ${response.statusCode}.");
//   }
// }

//Shared Pref Dashboard
Future<void> storeDashboardChartApitoCheckLoginSession(
    BuildContext context) async {
  final SharedPreferences prefs = await SharedPreferences.getInstance();
  final String token = prefs.getString('access_token') ?? '';

  Map<String, String> headers = {
    'Authorization': 'Bearer $token',
  };

  final Uri requestUri = Uri.parse(appBaseUrl + appDashboard);

  print('Initiating Dashboard API request...');
  try {
    final response = await http.get(requestUri, headers: headers);

    print("Response : " + response.toString());

    if (response.statusCode == 200) {
      print('Dashboard API request successful.');

      final Map<String, dynamic> data = jsonDecode(response.body);
      final List<dynamic> dataArray = data['data'];

      // Convert DataItem instances to JSON-compatible maps
      final List<Map<String, dynamic>> serializedData = dataArray
          .map((jsonData) => DataItem.fromJson(jsonData).toJson())
          .toList();

      // Store the serialized data in SharedPreferences
      await prefs.setString('dashboardChatModel', jsonEncode(serializedData));

      print('Dashboard data stored in SharedPreferences.');
    } else if (response.statusCode == 403) {
      // Decode the response body to access the detail message
      Map<String, dynamic> responseBody = json.decode(response.body);

      // Get the detail message from the response body
      String detailMessage = responseBody["detail"];
      print("API request session failed with status: ${response.statusCode}.");

      // Show the dialog to the user
      AwesomeDialog(
        dismissOnTouchOutside: false,
        context: context,
        dialogType: DialogType.info,
        animType: AnimType.bottomSlide,
        title: 'Session Expired!',
        desc: detailMessage,
        btnCancel: IconButton(
          onPressed: () {
            // Logout the user and perform necessary actions
            logout();
            final box = GetStorage();
            box.remove(LocalDBStrings.login_user);
            Get.offAll(() => LogIn());
          },
          icon: Image.asset(
            'asserts/icons/checked.png',
            width: 40,
          ),
          color: Colors.green,
        ),
      ).show();
    } else {
      print(
          "API request for session check failed with status: ${response.statusCode}.");
    }
  } catch (e) {
    print('Exception occurred: $e');
  }
}
// Future<void> storeDashboardChartApitoCheckLoginSession(
//     BuildContext context) async {
//   final SharedPreferences prefs = await SharedPreferences.getInstance();
//   final String token = prefs.getString('access_token') ?? '';
//   // final String token = '';

//   Map<String, String> headers = {
//     'Authorization': 'Bearer $token',
//   };
//   final response =
//       await http.get(Uri.parse(appBaseUrl + appDashboard), headers: headers);

//   print("Responce : " + response.toString());

//   if (response.statusCode == 200) {
//     // final jsonData = json.decode(response.body);
//     final Map<String, dynamic> data = jsonDecode(response.body);
//     final List<dynamic> dataArray = data['data'];

//     final List<DataItem> dashboardDataArray =
//         dataArray.map((jsonData) => DataItem.fromJson(jsonData)).toList();

//     final List<Map<String, dynamic>> serializedData = dashboardDataArray
//         .map((dashboardItem) => dashboardItem.toJson())
//         .toList();

//     print(serializedData);

//     //Save Dashboard data
//     // saveDashboardChatModelToPrefs(jsonData);
//     //

//     await prefs.setString('dashboardChatModel', jsonEncode(serializedData));
//   } else if (response.statusCode == 403) {
//     // Decode the response body to access the detail message
//     Map<String, dynamic> responseBody = json.decode(response.body);

//     // Get the detail message from the response body
//     String detailMessage = responseBody["detail"];
//     print("API request session failed with status: ${response.statusCode}.");
//     // Show the dialog to the user
//     AwesomeDialog(
//       dismissOnTouchOutside: false,
//       context: context,
//       dialogType: DialogType.info,
//       animType: AnimType.bottomSlide,
//       title: 'Session Expired!',
//       desc: detailMessage,
//       btnCancel: IconButton(
//         onPressed: () {
//           // Logout the user and perform necessary actions
//           logout();
//           final box = GetStorage();
//           box.remove(LocalDBStrings.login_user);
//           Get.offAll(() => LogIn());
//         },
//         icon: Image.asset(
//           'asserts/icons/checked.png',
//           width: 40,
//         ),
//         color: Colors.green,
//       ),
//     ).show();
//   } else {
//     print(
//         "API request doe session check failed with status: ${response.statusCode}.");
//   }
// }

//Shared Pref tracComlaintkList
Future<void> storeTracComlaintkList1() async {
  final SharedPreferences prefs = await SharedPreferences.getInstance();
  final String token = prefs.getString('access_token') ?? '';

  Map<String, String> headers = {
    'Authorization': 'Bearer $token',
  };

  final response = await http.get(Uri.parse(appBaseUrl + trackComplaintList),
      headers: headers);

  print("Responce1 : " + response.toString());

  if (response.statusCode == 200) {
    //  final Map<String, dynamic> responseData = json.decode(response.body);

    // return ComplaintListDetailModel.fromJson(responseData);
    // final jsonData = json.decode(response.body);
    final Map<String, dynamic> data = jsonDecode(response.body);
    final String page = data['next'];
    final int countTotal = data['count'];
    final List<dynamic> dataArray = data['results'];
    print("Total responce: ${data}.");
    final List<TrackComplaintItemModel> complaint_list_model = dataArray
        .map((jsonData) => TrackComplaintItemModel.fromJson(jsonData))
        .toList();

    final List<Map<String, dynamic>> serializedData = complaint_list_model
        .map((comlaintItemItem) => comlaintItemItem.toJson())
        .toList();
    print("Responce serializedData own complaint list : " +
        serializedData.toString());
    print('page no =' + page);

    //Save Dashboard data
    // saveDashboardChatModelToPrefs(jsonData);
    //

    await prefs.setString('trackComplaintListData', jsonEncode(serializedData));
    await prefs.setString('trackComplaintpagefirst', jsonEncode(page));
    await prefs.setInt('trackCountTotalfirst', countTotal);
    // await prefs.setString(
    //     'trackComplaintListDataMore', jsonEncode(serializedData));
  } else {
    print("API request failed with status: ${response.statusCode}.");
  }
}

//Shared Pref othersComlaintkList
Future<void> storeTracComlaintkList() async {
  final SharedPreferences prefs = await SharedPreferences.getInstance();
  final String token = prefs.getString('access_token') ?? '';

  Map<String, String> headers = {
    'Authorization': 'Bearer $token',
  };

  final Uri requestUri = Uri.parse(appBaseUrl + trackComplaintList);

  print('Initiating Track Complaint List API request...');
  try {
    final response = await http.get(requestUri, headers: headers);

    print("Response : " + response.toString());

    if (response.statusCode == 200) {
      print('Track Complaint List API request successful.');
      print('Track Complaint Url.' + requestUri.toString());
      print('Track Complaint Token.' + headers.toString());

      final Map<String, dynamic> data = jsonDecode(response.body);
      print("Response Data track complaint list : " + data.toString());
      final List<dynamic> dataArray = data['results'];
      final String? page = data['next'];
      final int? countTotal = data['count'];
      final List<TrackComplaintItemModel> trackComplaintList = dataArray
          .map((jsonData) => TrackComplaintItemModel.fromJson(jsonData))
          .toList();

      final List<Map<String, dynamic>> serializedData =
          trackComplaintList.map((item) => item.toJson()).toList();

      print("Serialized Data track complaint list : " +
          serializedData.toString());

      await prefs.setString('trackComplaintpageFirst', jsonEncode(page));
      await prefs.setInt('countTotalTrackFirst', countTotal ?? 0);
      await prefs.setString(
          'trackComplaintListData', jsonEncode(serializedData));

      print('Track Complaint List data stored in SharedPreferences.');
    } else {
      print("API request failed with status: ${response.statusCode}.");
    }
  } catch (e) {
    print('Exception occurred: $e');
  }
}

// Future<void> storeTracComlaintkList() async {
//   final SharedPreferences prefs = await SharedPreferences.getInstance();
//   final String token = prefs.getString('access_token') ?? '';

//   Map<String, String> headers = {
//     'Authorization': 'Bearer $token',
//   };
//   final response = await http.get(Uri.parse(appBaseUrl + trackComplaintList),
//       headers: headers);

//   print("Responce1 : " + response.toString());

//   if (response.statusCode == 200) {
//     //  final Map<String, dynamic> responseData = json.decode(response.body);

//     // return ComplaintListDetailModel.fromJson(responseData);
//     // final jsonData = json.decode(response.body);
//     final Map<String, dynamic> data = jsonDecode(response.body);
//     print("Responce Data track complaint list : " + data.toString());
//     final List<dynamic> dataArray = data['results'];
//     final String? page = data['next'];
//     final int? countTotal = data['count'];
//     final List<TrackComplaintItemModel> track_complaint_list_model = dataArray
//         .map((jsonData) => TrackComplaintItemModel.fromJson(jsonData))
//         .toList();

//     final List<Map<String, dynamic>> serializedData = track_complaint_list_model
//         .map((trackComlaintItemItem) => trackComlaintItemItem.toJson())
//         .toList();
//     print("Responce serializedData track complaint list : " +
//         serializedData.toString());
//     //  print(serializedData);

//     //Save Dashboard data
//     // saveDashboardChatModelToPrefs(jsonData);
//     //

//     await prefs.setString('trackComplaintpageFirst', jsonEncode(page));
//     await prefs.setInt('countTotalTrackFirst', countTotal!);

//     await prefs.setString('trackComplaintListData', jsonEncode(serializedData));
//     // await prefs.setString(
//     //     'othersComplaintListDataMore', jsonEncode(serializedData));
//   } else {
//     print("API request failed with status: ${response.statusCode}.");
//   }
// }

//Shared Pref othersComlaintkList
Future<void> storeOthersComlaintkList() async {
  final SharedPreferences prefs = await SharedPreferences.getInstance();
  final String token = prefs.getString('access_token') ?? '';

  Map<String, String> headers = {
    'Authorization': 'Bearer $token',
  };

  final Uri requestUri = Uri.parse(appBaseUrl + othersComplaintList);

  print('Initiating Others Complaint List API request...');
  try {
    final response = await http.get(requestUri, headers: headers);

    print("Response : " + response.toString());

    if (response.statusCode == 200) {
      print('Others Complaint List API request successful.');

      final Map<String, dynamic> data = jsonDecode(response.body);
      print("Response Data other complaint list : " + data.toString());
      final List<dynamic> dataArray = data['results'];
      final String? page = data['next'];
      final int? countTotal = data['count'];
      final List<OtherComplaintItemModel> othersComplaintList = dataArray
          .map((jsonData) => OtherComplaintItemModel.fromJson(jsonData))
          .toList();

      final List<Map<String, dynamic>> serializedData =
          othersComplaintList.map((item) => item.toJson()).toList();

      print("Serialized Data other complaint list : " +
          serializedData.toString());

      await prefs.setString('otherComplaintpageFirst', jsonEncode(page));
      await prefs.setInt('countTotalOtherFirst', countTotal ?? 0);
      await prefs.setString(
          'othersComplaintListData', jsonEncode(serializedData));

      print('Others Complaint List data stored in SharedPreferences.');
    } else {
      print("API request failed with status: ${response.statusCode}.");
    }
  } catch (e) {
    print('Exception occurred: $e');
  }
}
// Future<void> storeOthersComlaintkList() async {
//   final SharedPreferences prefs = await SharedPreferences.getInstance();
//   final String token = prefs.getString('access_token') ?? '';

//   Map<String, String> headers = {
//     'Authorization': 'Bearer $token',
//   };
//   final response = await http.get(Uri.parse(appBaseUrl + othersComplaintList),
//       headers: headers);

//   print("Responce1 : " + response.toString());

//   if (response.statusCode == 200) {
//     //  final Map<String, dynamic> responseData = json.decode(response.body);

//     // return ComplaintListDetailModel.fromJson(responseData);
//     // final jsonData = json.decode(response.body);
//     final Map<String, dynamic> data = jsonDecode(response.body);
//     print("Responce Data other complaint list : " + data.toString());
//     final List<dynamic> dataArray = data['results'];
//     final String? page = data['next'];
//     final int? countTotal = data['count'];
//     final List<OtherComplaintItemModel> others_complaint_list_model = dataArray
//         .map((jsonData) => OtherComplaintItemModel.fromJson(jsonData))
//         .toList();

//     final List<Map<String, dynamic>> serializedData =
//         others_complaint_list_model
//             .map((othersComlaintItemItem) => othersComlaintItemItem.toJson())
//             .toList();
//     print("Responce serializedData other complaint list : " +
//         serializedData.toString());
//     //  print(serializedData);

//     //Save Dashboard data
//     // saveDashboardChatModelToPrefs(jsonData);
//     //

//     await prefs.setString('otherComplaintpageFirst', jsonEncode(page));
//     await prefs.setInt('countTotalOtherFirst', countTotal!);

//     await prefs.setString(
//         'othersComplaintListData', jsonEncode(serializedData));
//     // await prefs.setString(
//     //     'othersComplaintListDataMore', jsonEncode(serializedData));
//   } else {
//     print("API request failed with status: ${response.statusCode}.");
//   }
// }

// complaint details
Future<void> storeComplaintDetailsData(List<String> userIds) async {
  try {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    final String token = prefs.getString('access_token') ?? '';

    Map<String, String> headers = {
      'Authorization': 'Bearer $token',
    };

    for (String userId in userIds) {
      final Uri requestUri = Uri.parse(appBaseUrl + complaintDetails + userId);
      final response = await http.get(requestUri, headers: headers);

      if (response.statusCode == 200) {
        final Map<String, dynamic> jsonData = json.decode(response.body);

        final ComplaintDetailModel complaintModel =
            ComplaintDetailModel.fromJson(jsonData);

        // Store in SharedPreferences with a unique key for each user
        // await prefs.setString(
        //   'complaintDetailsData_$userId',
        //   jsonEncode(complaintModel.toJson()),
        // );

        //

        // Store in SharedPreferences
        final prefs = await SharedPreferences.getInstance();

        prefs.setString('complaintDetailsData_$userId',
            jsonEncode(complaintModelToJson(complaintModel)));
        print("Complaint Detail data for user $userId stored successfully.");
      } else {
        print(
            "API request for Complaint Detail for user $userId failed with status: ${response.statusCode}.");
      }
    }
  } catch (e) {
    print("Error storing Complaint Detail data: $e");
  }
}
// Future<void> storeComplaintDetailsData(List<String> userIds) async {
//   try {
//     final SharedPreferences prefs = await SharedPreferences.getInstance();
//     final String token = prefs.getString('access_token') ?? '';

//     Map<String, String> headers = {
//       'Authorization': 'Bearer $token',
//     };

//     for (String userId in userIds) {
//       final response = await http.get(
//         Uri.parse(appBaseUrl + complaintDetails + userId),
//         headers: headers,
//       );

//       if (response != null && response.statusCode == 200) {
//         final Map<String, dynamic> jsonData = json.decode(response.body);

//         final ComplaintDetailModel complaintModel =
//             ComplaintDetailModel.fromJson(jsonData);

//         // Store in SharedPreferences with a unique key for each user
//         // await storeDataInSharedPreferences('complaintDetailsData_$userId', complaintModel);
//         // Store in SharedPreferences
//         final prefs = await SharedPreferences.getInstance();

//         prefs.setString('complaintDetailsData_$userId',
//             jsonEncode(complaintModelToJson(complaintModel)));
//         print(" storing Complaint Detail data");
//       } else {
//         print(
//             "API request for Complaint Detail for user $userId failed with status: ${response?.statusCode}.");
//       }
//     }
//   } catch (e) {
//     print("Error storing Complaint Detail data: $e");
//   }
// }

// Future<void> storeComplaintDetailData(String userId) async {
//   try {
//     final SharedPreferences prefs = await SharedPreferences.getInstance();
//     final String token = prefs.getString('access_token') ?? '';

//     Map<String, String> headers = {
//       'Authorization': 'Bearer $token',
//     };

//     final response = await http.get(
//       Uri.parse(appBaseUrl + complaintDetails + userId),
//       headers: headers,
//     );

//     if (response.statusCode == 200) {
//       //

//       final Map<String, dynamic> jsonData = json.decode(response.body);

//       final ComplaintDetailModel complaintModel =
//           ComplaintDetailModel.fromJson(jsonData);

//       // Store in SharedPreferences
//       final prefs = await SharedPreferences.getInstance();

//       prefs.setString('complaintDetailsData',
//           jsonEncode(complaintModelToJson(complaintModel)));
//     } else {
//       print(
//           "API request for Complaint Detail failed with status: ${response.statusCode}.");
//     }
//   } catch (e) {
//     print("Error storing Complaint Detail data: $e");
//   }
// }
// complaint comment details
Future<void> storeComplaintDetailComentsData(String userId) async {
  try {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    final String token = prefs.getString('access_token') ?? '';

    Map<String, String> headers = {
      'Authorization': 'Bearer $token',
    };

    final Uri requestUri =
        Uri.parse(appBaseUrl + complaintCommnentsDetails + userId);
    final http.Response response = await http.get(requestUri, headers: headers);

    if (response.statusCode == 200) {
      final Map<String, dynamic> data = jsonDecode(response.body);
      final List<dynamic> dataArray = data['data_array'];

      final List<ComplaintActionCommentsItemModel> commentsList = dataArray
          .map(
              (jsonData) => ComplaintActionCommentsItemModel.fromJson(jsonData))
          .toList();

      final List<Map<String, dynamic>> serializedData =
          commentsList.map((commentItem) => commentItem.toJson()).toList();

      await prefs.setString(
          'complaintCommentsDetailsData', jsonEncode(serializedData));

      print("Complaint Comments data stored successfully for user $userId.");
    } else {
      print(
          "API request for Complaint Comments failed with status: ${response.statusCode}.");
    }
  } catch (e) {
    print("Error storing Complaint Comments data: $e");
  }
}
// Future<void> storeComplaintDetailComentsData(String userId) async {
//   try {
//     final SharedPreferences prefs = await SharedPreferences.getInstance();
//     final String token = prefs.getString('access_token') ?? '';

//     Map<String, String> headers = {
//       'Authorization': 'Bearer $token',
//     };

//     final response = await http.get(
//       Uri.parse(appBaseUrl + complaintCommnentsDetails + userId),
//       headers: headers,
//     );

//     if (response.statusCode == 200) {
//       final Map<String, dynamic> data = jsonDecode(response.body);
//       final List<dynamic> dataArray = data['data_array'];

//       final List<ComplaintActionCommentsItemModel> others_complaint_list_model =
//           dataArray
//               .map((jsonData) =>
//                   ComplaintActionCommentsItemModel.fromJson(jsonData))
//               .toList();

//       final List<Map<String, dynamic>> serializedData =
//           others_complaint_list_model
//               .map((othersComlaintItemItem) => othersComlaintItemItem.toJson())
//               .toList();

//       //Save Dashboard data
//       // saveDashboardChatModelToPrefs(jsonData);
//       //
//       print("API request for Complaint Detail with status: $serializedData");

//       await prefs.setString(
//           'complaintCommentsDetailsData', jsonEncode(serializedData));
//     } else {
//       print(
//           "API request for Complaint Detail failed with status: ${response.statusCode}.");
//     }
//   } catch (e) {
//     print("Error storing Complaint Detail data: $e");
//   }
// }

// Future<void> storeComplaintDetailImageData(String userId) async {
//   try {
//     final SharedPreferences prefs = await SharedPreferences.getInstance();
//     final String token = prefs.getString('access_token') ?? '';

//     Map<String, String> headers = {
//       'Authorization': 'Bearer $token',
//     };

//     final response = await http.get(
//       Uri.parse(appBaseUrl + complaintComnetsImageDetails + userId),
//       headers: headers,
//     );

//     if (response.statusCode == 200) {
//       final Map<String, dynamic> data = jsonDecode(response.body);
//       final List<dynamic> dataArray = data['data_array'];

//       final List<ImageDataArray> others_complaint_list_model = dataArray
//           .map((jsonData) => ImageDataArray.fromJson(jsonData))
//           .toList();

//       final List<Map<String, dynamic>> serializedData =
//           others_complaint_list_model
//               .map((othersComlaintItemItem) => othersComlaintItemItem.toJson())
//               .toList();
//       // Save images to local storage
//       await saveImagesLocally(others_complaint_list_model);

//       //Save Dashboard data
//       // saveDashboardChatModelToPrefs(jsonData);
//       //
//       print("API request for Complaint Detail with status: $serializedData");

//       await prefs.setString(
//           'complaintImageDetailsData', jsonEncode(serializedData));
//     } else {
//       print(
//           "API request for Complaint Detail failed with status: ${response.statusCode}.");
//     }
//   } catch (e) {
//     print("Error storing Complaint Detail data: $e");
//   }
// }

Future<void> saveImagesLocally(List<ImageDataArray> imageDetailsList) async {
  try {
    Directory appDocumentsDirectory = await getApplicationDocumentsDirectory();
    String imagesDirectoryPath =
        "${appDocumentsDirectory.path}/CTComplaintDetailsImages";
    Directory(imagesDirectoryPath).createSync(recursive: true);

    List<String> savedPaths = [];

    for (ImageDataArray imageDetails in imageDetailsList) {
      String imageUrl = imageDetails.attachment;
      String fileName = "image_${imageDetails.id}.jpg";

      File file = File("$imagesDirectoryPath/$fileName");
      final response = await http.get(Uri.parse(appBaseUrl + imageUrl));

      if (response.statusCode == 200) {
        await file.writeAsBytes(response.bodyBytes);
        savedPaths.add(file.path); // Save the path
        print('Saved ' + file.path);
      }
    }

    // Save paths to SharedPreferences
    SharedPreferences prefs = await SharedPreferences.getInstance();
    prefs.setStringList('savedImagePaths', savedPaths);
  } catch (e) {
    print("Error saving images locally: $e");
  }
}
