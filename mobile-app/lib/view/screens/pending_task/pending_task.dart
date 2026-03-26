import 'dart:convert';
import 'dart:math';

import 'package:connectivity/connectivity.dart';
import 'package:dha_ctt_app/constant.dart';
import 'package:dha_ctt_app/model/resources/string_manager.dart';
import 'package:dha_ctt_app/model/resources/values_manager.dart';
import 'package:dha_ctt_app/view/screens/dashboard/home.dart';
import 'package:dha_ctt_app/view/widgets/app_bar/custom_app_bar.dart';
import 'package:dha_ctt_app/view/widgets/dialogs/custom_dialog.dart';
import 'package:dha_ctt_app/view/widgets/dialogs/custom_toast.dart';
import 'package:dha_ctt_app/view_model/view_models/new_complaint_model/category_model.dart';
import 'package:dha_ctt_app/view_model/view_models/qa_checklist/qa_checklist_model.dart';
import 'package:dio/dio.dart';
import 'package:dropdown_textfield/dropdown_textfield.dart';
import 'package:flutter/material.dart';
import 'package:overlay_loader_with_app_icon/overlay_loader_with_app_icon.dart';
import 'package:shared_preferences/shared_preferences.dart';

// Future<bool> isInternetConnected() async {
//   var connectivityResult = await (Connectivity().checkConnectivity());
//   return connectivityResult != ConnectivityResult.none;
// }

class PendingTask extends StatefulWidget {
  const PendingTask({super.key});

  @override
  _PendingTaskState createState() => _PendingTaskState();
}

class _PendingTaskState extends State<PendingTask> {
  bool isInternetConnected = false;
  List<String> queuedComplaints = [];
  final Connectivity _connectivity = Connectivity();
  String appBaseUrl = AppStrings.appBaseUrl;
  String appNewcomplaint = AppStrings.NEW_COMPLAINT;
  String appQAchecklist = AppStrings.QA_CHECKLIST;
  String appGetCategory = AppStrings.GET_CATEGORY;
  String appComplaintStatuses = AppStrings.COMPLAINT_STATUS;

  SingleValueDropDownController? _cnt;
  SingleValueDropDownController? _Subcnt;
  List<Item> chatagoriDataArray = [];
  List<Item> allchatagoriData = [];
  bool _isLoading = false;

  List<QAChecklistItem> qachatagoriDataArray = [];
  List<QAChecklistItem> allqachatagoriData = [];

  // Function to retrieve categories from SharedPreferences and populate the list
  Future<void> getCategoriesFromSharedPreferences() async {
    try {
      final SharedPreferences prefs = await SharedPreferences.getInstance();
      final String? serializedData = prefs.getString('chatagoriDataArray');

      if (serializedData != null && serializedData.isNotEmpty) {
        final List<dynamic> dataArray = jsonDecode(serializedData);

        chatagoriDataArray =
            dataArray.map((json) => Item.fromJson(json)).toList();

        // Update the dropdown lists if needed
        List<Item> updatedDropDownList = [];
        chatagoriDataArray.forEach((status) {
          // Use the category id as the value and the name as the name
          // Check if the category id is 0 before adding to the list

          updatedDropDownList.add(status);

          // print("Step 2: ${updatedDropDownList}");
        });

        setState(() {
          allchatagoriData =
              updatedDropDownList; // Update the category dropdown list

          //     selectedCategory); // Update the subcategory dropdown list
        });
      } else {
        print('No category data found in SharedPreferences.');
      }
    } catch (e) {
      print('Error retrieving category data from SharedPreferences: $e');
    }
  }

// Function to retrieve categories from SharedPreferences and populate the list
  Future<void> getQACategoriesFromSharedPreferences() async {
    try {
      final SharedPreferences prefs = await SharedPreferences.getInstance();
      final String? serializedData = prefs.getString('qachatagoriDataArray');

      if (serializedData != null && serializedData.isNotEmpty) {
        final List<dynamic> dataArray = jsonDecode(serializedData);

        qachatagoriDataArray =
            dataArray.map((json) => QAChecklistItem.fromJson(json)).toList();

        // Update the dropdown lists if needed
        List<QAChecklistItem> updatedDropDownList = [];
        qachatagoriDataArray.forEach((item) {
          // Use the category id as the value and the name as the name
          // Check if the category id is 0 before adding to the list

          updatedDropDownList.add(item);

          // print("Step 2: ${updatedDropDownList}");
        });

        setState(() {
          allqachatagoriData =
              updatedDropDownList; // Update the category dropdown list
        });
      } else {
        print('No category data found in SharedPreferences.');
      }
    } catch (e) {
      print('Error retrieving QA category data from SharedPreferences: $e');
    }
  }

  Future<bool> isInternetConnect() async {
    var connectivityResult = await (Connectivity().checkConnectivity());
    return connectivityResult != ConnectivityResult.none;
  }

  void checkInternetConnectivity() async {
    print("internet checking");
    var connectivityResult = await Connectivity().checkConnectivity();
    setState(() {
      isInternetConnected = connectivityResult != ConnectivityResult.none;
    });
  }

  void loadQueuedComplaints() async {
    print("executing loadQueuedComplaints ");
    final prefs = await SharedPreferences.getInstance();
    queuedComplaints = prefs.getStringList('queued_complaints') ?? [];
  }

  Future<void> postPendingComplaints() async {
    print("pending is running");
    if (isInternetConnected && queuedComplaints.isNotEmpty) {
      List<String> successfullyPostedComplaints = [];

      for (var complaint in queuedComplaints) {
        print(complaint);
        bool isPosted = await processQueuedComplaint(complaint);

        if (isPosted) {
          successfullyPostedComplaints.add(complaint);
        }
      }

      // Remove successfully posted complaints from the queue
      queuedComplaints.removeWhere(
          (complaint) => successfullyPostedComplaints.contains(complaint));

      // Save the updated queue
      await saveQueuedComplaints(queuedComplaints);
    }
  }

  Future<bool> processQueuedComplaint(String complaint) async {
    // Parse the JSON complaint string into a Map
    Map<String, dynamic> complaintData = jsonDecode(complaint);
    print(complaint);
    // Now you have the complaint data as a JSON object, and you can pass it to postQueuedComplaint
    bool isPosted = await postQueuedComplaint(complaintData);

    return isPosted;
  }

  Future<void> saveQueuedComplaints(List<String> complaints) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setStringList('queued_complaints', complaints);
    print("something");
  }

  Future<bool> postQueuedComplaint(Map<String, dynamic> complaintData) async {
    print("Running the queue");
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    final String token = prefs.getString('access_token') ?? '';

    if (token.isEmpty) {
      print('Access token is empty');
      return false; // Return false to indicate an error
    }

    Map<String, String> headers = {
      'Authorization': 'Bearer $token',
    };

    var random = Random();
    var boundary = '---------------------------${random.nextInt(1000000000)}';
    headers['Content-Type'] = 'multipart/form-data; boundary=$boundary';

    try {
      var dio = Dio();
      FormData formData = FormData.fromMap({
        'status_id': complaintData['status_id'].toString(),
        'category_id': complaintData['category_id'].toString(),
        'subcategory_id': complaintData['subcategory_id'].toString(),
        'area_id': complaintData['area_id'].toString(),
        'description': complaintData['description'].toString(),
        'latitude': complaintData['latitude'].toString(),
        'longitude': complaintData['longitude'].toString(),
        'attachments':
            await MultipartFile.fromFile(complaintData['attachments']),
      });

      var response = await dio.post(
        appBaseUrl + appNewcomplaint,
        data: formData,
        options: Options(
          headers: headers,
        ),
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        return true; // Return true to indicate success
      } else {
        return false; // Return false to indicate an error
      }
    } catch (e) {
      print('Error while posting queued complaint: $e');
      return false; // Return false to indicate an error
    }
  }

// posting  Compalint
  Future<void> postComplaintData(Map<String, dynamic> complaint) async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    final String token = prefs.getString('access_token') ?? '';

    if (token.isEmpty) {
      print('Access token is empty');
      return;
    }

    Map<String, String> headers = {
      'Authorization': 'Bearer $token',
    };

    // Create a Random instance to generate a boundary
    var random = Random();
    var boundary = '---------------------------${random.nextInt(1000000000)}';

    // Set Content-Type with boundary parameter
    headers['Content-Type'] = 'multipart/form-data; boundary=$boundary';

    // Create a FormData object to send as the request body
    var formData = FormData.fromMap({
      'status_id': complaint['status_id'].toString(),
      'category_id': complaint['category_id'].toString(),
      'subcategory_id': complaint['subcategory_id'].toString(),
      'area_id': complaint['area_id'].toString(),
      'description': complaint['description'].toString(),
      'latitude': complaint['latitude'].toString(),
      'longitude': complaint['longitude'].toString(),
      'attachments': await MultipartFile.fromFile(complaint['attachments']),
    });

    print("Selected TagId: ${complaint['tagId'].toString()}");
    print("Selected Status: ${complaint['status_id'].toString()}");
    print("Selected Category: ${complaint['category_id'].toString()}");
    print("Selected Subcategory: ${complaint['subcategory_id'].toString()}");
    print("Selected Area: ${complaint['area_id'].toString()}");
    print("Selected Description: ${complaint['description'].toString()}");

    print("Selected latitude: ${complaint['latitude'].toString()}");
    print("Selected longitude: ${complaint['longitude'].toString()}");

    //rome shred
    // deleteComplaintFromSharedPreferences(complaint);

    // Send the request using Dio (an HTTP client for Dart)
    var dio = Dio();
    var response = await dio.post(
      appBaseUrl + appNewcomplaint,
      data: formData,
      options: Options(
        headers: headers,
      ),
    );

    print("Response Data: ${response.data}");

    if (response.statusCode == 200 || response.statusCode == 201) {
      print("Data Upload Successfully....");
      // showAnimatedCheckmarkDialog(
      //     context, 'Data Uploaded Successfully!', appcolor);
      // // _isLoading = false;
      // await Future.delayed(Duration(seconds: 1));
      funToast("Data Uploaded Successfully!", appcolor);

      final route = MaterialPageRoute(builder: (context) => Home());
      Navigator.pushAndRemoveUntil(context, route, (route) => false);
    } else {
      // _isLoading = false;
      // Error handling

      print('API Error: ${response.statusCode}+${response.data}');

      // Show a simple dialog with the API error message
      showDialog(
        context: context,
        builder: (BuildContext context) {
          return SimpleDialog(
            title: Text('Server Side Issue!'),
            children: <Widget>[
              SimpleDialogOption(
                onPressed: () {
                  Navigator.of(context).pop(); // Close the dialog
                },
                child: Text(
                    'Something Went Wrong! ' + response.statusCode.toString()),
              ),
            ],
          );
        },
      );
    }
  }

  Future<void> postQAComplaintData(Map<String, dynamic> qacomplaint) async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    final String token = prefs.getString('access_token') ?? '';

    if (token.isEmpty) {
      print('Access token is empty');
      return;
    }
    print(token);

    Map<String, String> headers = {
      'Authorization': 'Bearer $token',
    };

    // Create a Random instance to generate a boundary
    var random = Random();
    var boundary = '---------------------------${random.nextInt(1000000000)}';

    // Set Content-Type with boundary parameter
    headers['Content-Type'] = 'multipart/form-data; boundary=$boundary';

    // Create a FormData object to send as the request body
    var formData = FormData.fromMap({
      // 'status_id': _statusId.toString(),
      // 'subcategory_id': _subCatID.toString(),
      'category_id': qacomplaint['subcategory_id'].toString(),
      'area_id': qacomplaint['area_id'].toString(),
      'rating': qacomplaint['rating'].toString(),
      'latitude': qacomplaint['latitude'].toString(),
      'longitude': qacomplaint['longitude'].toString(),
      'attachments': await MultipartFile.fromFile(qacomplaint['attachments']),
    });

    print("Selected TagId: ${qacomplaint['tagId'].toString()}");
    // print("Selected Tag: ${qacomplaint['tag'].toString()}");
    print("Selected Subcategory: ${qacomplaint['subcategory_id'].toString()}");
    print("Selected Category: ${qacomplaint['category_id'].toString()}");
    print("Selected Area: ${qacomplaint['area_id'].toString()}");
    print("Selected rating: ${qacomplaint['rating'].toString()}");

    print("Selected latitude: ${qacomplaint['latitude'].toString()}");
    print("Selected longitude: ${qacomplaint['longitude'].toString()}");
    // printSelectedValues();

    // Send the request using Dio (an HTTP client for Dart)
    var dio = Dio();
    var response = await dio.post(
      appBaseUrl + appQAchecklist,
      data: formData,
      options: Options(
        headers: headers,
      ),
    );

    if (response.statusCode == 200 || response.statusCode == 201) {
      print("Data Upload Successfully....");
      // final responseData = response.data;
      // Map<String, dynamic> responseJson = json.decode(responseData);

      // print("Responce Json: ${responseJson}");

      // showAnimatedCheckmarkDialog(
      //     context, 'Data Uploaded Successfully!', appcolor);
      // // _isLoading = false;
      // await Future.delayed(Duration(seconds: 1));
      funToast("Data Uploaded Successfully!", appcolor);

      final route = MaterialPageRoute(builder: (context) => Home());
      Navigator.pushAndRemoveUntil(context, route, (route) => false);
    } else {
      // _isLoading = false;
      // Error handling

      print('API Error: ${response.statusCode}+${response.data}');

      // Show a simple dialog with the API error message
      showDialog(
        context: context,
        builder: (BuildContext context) {
          return SimpleDialog(
            title: Text('Server Side Issue!'),
            children: <Widget>[
              SimpleDialogOption(
                onPressed: () {
                  Navigator.of(context).pop(); // Close the dialog
                },
                child: Text(
                    'Something Went Wrong! ' + response.statusCode.toString()),
              ),
            ],
          );
        },
      );
    }
  }

//Remove Complaint
  Future<void> removeComplaint(int index) async {
    final prefs = await SharedPreferences.getInstance();
    final List<String> queuedComplaints =
        prefs.getStringList('queued_complaints') ?? [];

    if (index >= 0 && index < queuedComplaints.length) {
      queuedComplaints.removeAt(index);
      await prefs.setStringList('queued_complaints', queuedComplaints);
    }
  }

  Future<void> removeAndpostComplaintAndQAdata(
      {required int index,
      required Map<String, dynamic> qacomplaint,
      required Map<String, dynamic> complaint}) async {
    final prefs = await SharedPreferences.getInstance();
    final String token = prefs.getString('access_token') ?? '';

    //Store in Shared
    final List<String> queuedComplaints =
        prefs.getStringList('queued_complaints') ?? [];

    if (token.isEmpty) {
      print('Access token is empty');
      return;
    }

    Map<String, String> headers = {
      'Authorization': 'Bearer $token',
    };
    // Create a Random instance to generate a boundary
    var random = Random();
    var boundary = '---------------------------${random.nextInt(1000000000)}';

    // Set Content-Type with boundary parameter
    headers['Content-Type'] = 'multipart/form-data; boundary=$boundary';

    if (index >= 0 && index < queuedComplaints.length) {
      if (jsonDecode(queuedComplaints[index])['tag'] == "Complaint") {
        // Create a FormData object to send as the request body
        var formData = FormData.fromMap({
          'status_id': complaint['status_id'].toString(),
          'category_id': complaint['category_id'].toString(),
          'subcategory_id': complaint['subcategory_id'].toString(),
          'area_id': complaint['area_id'].toString(),
          'description': complaint['description'].toString(),
          'latitude': complaint['latitude'].toString(),
          'longitude': complaint['longitude'].toString(),
          'attachments': await MultipartFile.fromFile(complaint['attachments']),
        });

        // Send the request using Dio (an HTTP client for Dart)
        var dio = Dio();
        var response = await dio.post(
          appBaseUrl + appNewcomplaint,
          data: formData,
          options: Options(
            headers: headers,
          ),
        );

        print("Response Data: ${response.data}");

        if (response.statusCode == 200 || response.statusCode == 201) {
          print("Data Upload Successfully....");
          // showAnimatedCheckmarkDialog(
          //     context, 'Data Uploaded Successfully!', appcolor);
          // _isLoading = false;
          // await Future.delayed(Duration(seconds: 1));
          funToast("Data Uploaded Successfully!", appcolor);

          final route = MaterialPageRoute(builder: (context) => Home());
          Navigator.pushAndRemoveUntil(context, route, (route) => false);
        } else {
          _isLoading = false;
          // Error handling

          print('API Error: ${response.statusCode}+${response.data}');

          // Show a simple dialog with the API error message
          showDialog(
            context: context,
            builder: (BuildContext context) {
              return SimpleDialog(
                title: Text('Server Side Issue!'),
                children: <Widget>[
                  SimpleDialogOption(
                    onPressed: () {
                      Navigator.of(context).pop(); // Close the dialog
                    },
                    child: Text('Something Went Wrong! ' +
                        response.statusCode.toString()),
                  ),
                ],
              );
            },
          );
        }
      } else {
        var formData = FormData.fromMap({
          // 'status_id': _statusId.toString(),
          // 'subcategory_id': _subCatID.toString(),
          'category_id': qacomplaint['subcategory_id'].toString(),
          'area_id': qacomplaint['area_id'].toString(),
          'rating': qacomplaint['rating'].toString(),
          'latitude': qacomplaint['latitude'].toString(),
          'longitude': qacomplaint['longitude'].toString(),
          'attachments':
              await MultipartFile.fromFile(qacomplaint['attachments']),
        });

        // Send the request using Dio (an HTTP client for Dart)
        var dio = Dio();
        var response = await dio.post(
          appBaseUrl + appQAchecklist,
          data: formData,
          options: Options(
            headers: headers,
          ),
        );

        if (response.statusCode == 200 || response.statusCode == 201) {
          print("Data Upload Successfully....");

          // showAnimatedCheckmarkDialog(
          //     context, 'Data Uploaded Successfully!', appcolor);
          // // _isLoading = false;
          // await Future.delayed(Duration(seconds: 1));
          funToast("Data Uploaded Successfully!", appcolor);

          final route = MaterialPageRoute(builder: (context) => Home());
          Navigator.pushAndRemoveUntil(context, route, (route) => false);
        } else {
          // _isLoading = false;
          // Error handling

          print('API Error: ${response.statusCode}+${response.data}');

          // Show a simple dialog with the API error message
          showDialog(
            context: context,
            builder: (BuildContext context) {
              return SimpleDialog(
                title: Text('Server Side Issue!'),
                children: <Widget>[
                  SimpleDialogOption(
                    onPressed: () {
                      Navigator.of(context).pop(); // Close the dialog
                    },
                    child: Text('Something Went Wrong! ' +
                        response.statusCode.toString()),
                  ),
                ],
              );
            },
          );
        }
      }
      queuedComplaints.removeAt(index);
      await prefs.setStringList('queued_complaints', queuedComplaints);
    }
  }

  void initState() {
    super.initState();

// SharedPreferences pref =await SharedPreferences.getInstance();
// await pref.clear();

    // Initialize the internet connectivity status
    checkInternetConnectivity();
    // Load queued complaints
    loadQueuedComplaints();
    getCategoriesFromSharedPreferences();
    getQACategoriesFromSharedPreferences();
  }

  @override
  Widget build(BuildContext context) {
    DateTime currentDateTime = DateTime.now();
    double scWidth = MediaQuery.of(context).size.width;

    // String complaintCat ="";
    // String complaintSubCat ="";
    // String qacomplaintCat ="";
    // String qacomplaintSubCat ="";

    return WillPopScope(
      onWillPop: () async {
        Navigator.pushAndRemoveUntil(
          context,
          MaterialPageRoute(builder: (context) => Home()),
          (route) =>
              false, // This predicate removes all routes, making it impossible to navigate back
        );
        return true;
      },
      child: Scaffold(
          appBar: CustomAppBar(
              navFunction: () {
                Navigator.pushAndRemoveUntil(
                  context,
                  MaterialPageRoute(builder: (context) => Home()),
                  (route) =>
                      false, // This predicate removes all routes, making it impossible to navigate back
                );
              },
              lastIcon: Icons.info_outline,
              infoFunction: () {
                CustomDialog(context);
              }),
          body: OverlayLoaderWithAppIcon(
            overlayBackgroundColor: appcolor,
            isLoading: false,
            appIcon: Image.asset(
              "asserts/icons/app_icon.png",
              width: 40,
            ),
            child: Container(
              alignment: Alignment.center,
              child: Column(
                children: [
                  Container(
                    // color: appcolorAq,
                    width: scWidth,
                    alignment: Alignment.center,
                    decoration: BoxDecoration(
                        borderRadius:
                            BorderRadius.all(Radius.circular(roundCardView))),
                    margin: EdgeInsets.only(
                      bottom: marginLR,
                    ),
                    padding: EdgeInsets.only(top: 0, bottom: 0),
                    child: Container(
                      width: scWidth,
                      alignment: Alignment.center,
                      color: appcolorlabel,
                      child: Padding(
                        padding: const EdgeInsets.all(2.0),
                        child: Text(
                          "Pending List",
                          style: TextStyle(
                            color: dfColor,
                            fontWeight: FontWeight.w600,
                            fontSize: dfFontSize - 2,
                          ),
                        ),
                      ),
                    ),
                  ),

                  // Container(
                  //   margin: EdgeInsets.only(top: marginLR + marginSet),
                  //   child: Text(
                  //     'Pending List',
                  //     style: TextStyle(
                  //       fontSize: lgFontSize,
                  //       color: appcolor,
                  //       fontWeight: FontWeight.bold,
                  //     ),
                  //   ),
                  // ),
                  SizedBox(height: 5),
                  (queuedComplaints.isNotEmpty)
                      ? Expanded(
                          child: ListView.builder(
                            itemCount: queuedComplaints.length,
                            itemBuilder: (BuildContext context, int i) {
                              print(queuedComplaints);
                              return Container(
                                margin: EdgeInsets.symmetric(
                                  horizontal: marginLR,
                                  vertical: marginSet,
                                ),
                                child: Card(
                                  elevation: 8,
                                  color: redAlert,
                                  shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(
                                      roundCardView,
                                    ),
                                  ),
                                  child: ListTile(
                                    contentPadding: EdgeInsets.all(0),
                                    title: Row(
                                      crossAxisAlignment:
                                          CrossAxisAlignment.center,
                                      children: [
                                        Image.asset(
                                          'asserts/icons/ic_timeline.png',
                                          width: scWidth / 9,
                                        ),
                                        // SizedBox(width: 10),
                                        Column(
                                          children: [
                                            SizedBox(
                                              width: scWidth / 2,
                                              child: Text(
                                                softWrap: true,
                                                overflow: TextOverflow.ellipsis,
                                                jsonDecode(queuedComplaints[i])[
                                                            'category_id'] ==
                                                        allchatagoriData[i].id
                                                    ? ""
                                                    : "Category : " +
                                                        allchatagoriData[i]
                                                            .name,
                                                style: TextStyle(
                                                  fontSize: AppSize.s14,
                                                  fontWeight: FontWeight.w700,
                                                ),
                                              ),
                                            ),
                                            SizedBox(
                                              width: scWidth / 2,
                                              child: Text(
                                                jsonDecode(queuedComplaints[i])[
                                                            'subcategory_id'] ==
                                                        allchatagoriData[i].id
                                                    ? ""
                                                    : "Sub Cat : " +
                                                        allchatagoriData[i]
                                                            .name,
                                                softWrap: true,
                                                overflow: TextOverflow.ellipsis,
                                                style: TextStyle(
                                                  fontWeight: FontWeight.w500,
                                                  fontSize: AppSize.s13,
                                                ),
                                              ),
                                            ),
                                            jsonDecode(queuedComplaints[i])[
                                                        'tag'] !=
                                                    "Complaint"
                                                ? Container()
                                                : SizedBox(
                                                    width: scWidth / 2,
                                                    child: Text(
                                                      "Description : " +
                                                          jsonDecode(
                                                                  queuedComplaints[
                                                                      i])[
                                                              'description'],
                                                      softWrap: true,
                                                      overflow:
                                                          TextOverflow.ellipsis,
                                                      style: TextStyle(
                                                        fontSize: AppSize.s12,
                                                      ),
                                                    ),
                                                  ),
                                          ],
                                        ),
                                        Spacer(),
                                        GestureDetector(
                                          child: Icon(Icons.upload),
                                          onTap: () async {
                                            SharedPreferences prefs =
                                                await SharedPreferences
                                                    .getInstance();

                                            bool internetConnected =
                                                await isInternetConnect();
                                            if (internetConnected) {
                                              if (jsonDecode(
                                                          queuedComplaints[i])[
                                                      'tag'] ==
                                                  'Complaint') {
                                                Map<String, dynamic>
                                                    complaintData = {
                                                  'tagId': jsonDecode(
                                                          queuedComplaints[i])[
                                                      'tagId'],
                                                  'status_id': jsonDecode(
                                                          queuedComplaints[i])[
                                                      'status_id'],
                                                  'category_id': jsonDecode(
                                                          queuedComplaints[i])[
                                                      'category_id'],
                                                  'subcategory_id': jsonDecode(
                                                          queuedComplaints[i])[
                                                      'subcategory_id'],
                                                  'area_id': jsonDecode(
                                                          queuedComplaints[i])[
                                                      'area_id'],
                                                  'description': jsonDecode(
                                                          queuedComplaints[i])[
                                                      'description'],
                                                  'latitude': jsonDecode(
                                                          queuedComplaints[i])[
                                                      'latitude'],
                                                  'longitude': jsonDecode(
                                                          queuedComplaints[i])[
                                                      'longitude'],
                                                  'attachments': jsonDecode(
                                                          queuedComplaints[i])[
                                                      'attachments'],
                                                };

                                                // Call your function to post the complaint
                                                postComplaintData(
                                                    complaintData);
                                              } else {
                                                //QA
                                                Map<String, dynamic>
                                                    qacomplaintData = {
                                                  'tagId': jsonDecode(
                                                          queuedComplaints[i])[
                                                      'tagId'],
                                                  'area_id': jsonDecode(
                                                          queuedComplaints[i])[
                                                      'area_id'],
                                                  'category_id': jsonDecode(
                                                          queuedComplaints[i])[
                                                      'category_id'],
                                                  'subcategory_id': jsonDecode(
                                                          queuedComplaints[i])[
                                                      'subcategory_id'],
                                                  'rating': jsonDecode(
                                                          queuedComplaints[i])[
                                                      'rating'],
                                                  // 'description': jsonDecode(
                                                  //     queuedComplaints[i])['description'],
                                                  'latitude': jsonDecode(
                                                          queuedComplaints[i])[
                                                      'latitude'],
                                                  'longitude': jsonDecode(
                                                          queuedComplaints[i])[
                                                      'longitude'],
                                                  'attachments': jsonDecode(
                                                          queuedComplaints[i])[
                                                      'attachments'],
                                                };

                                                //call qa complaint
                                                postQAComplaintData(
                                                    qacomplaintData);
                                              }
                                              print("Press");

                                              //Removeing the Complaint from queues
                                              removeComplaint(i);
                                            } else {
                                              funToast(
                                                  "No Internet Connectivity! ",
                                                  appcolor);
                                            }
                                          },
                                        ),
                                        Container(
                                          // color: Colors.amber,
                                          // margin: EdgeInsets.only(bottom: 10),
                                          child: Image.asset(
                                            jsonDecode(queuedComplaints[i])[
                                                        'tag'] ==
                                                    "Complaint"
                                                ? 'asserts/icons/ic_complaint_banner.png'
                                                : 'asserts/icons/ic_qa_checklist_banner.png',
                                            width: scWidth / 5.9,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                ),
                              );
                            },
                          ),
                        )
                      : Container(
                          margin: EdgeInsets.only(top: scWidth / 1.5),
                          alignment: Alignment.center,
                          child: Text(
                            "No Pending Task Available!",
                            style: TextStyle(
                                color: appcolor,
                                fontSize: dfFontSize,
                                fontWeight: FontWeight.normal),
                          ),
                        ),
                ],
              ),
            ),
          ),
          floatingActionButton: (queuedComplaints.isNotEmpty)
              ? FloatingActionButton(
                  onPressed: () async {
                    bool internetConnected = await isInternetConnect();

                    if (internetConnected) {
                      setState(() {
                        _isLoading = true;
                      });
                      for (int i = 0; i < queuedComplaints.length; i++) {
                        Map<String, dynamic> complaintData = {
                          'tagId': jsonDecode(queuedComplaints[i])['tagId'],
                          'status_id':
                              jsonDecode(queuedComplaints[i])['status_id'],
                          'category_id':
                              jsonDecode(queuedComplaints[i])['category_id'],
                          'subcategory_id':
                              jsonDecode(queuedComplaints[i])['subcategory_id'],
                          'area_id': jsonDecode(queuedComplaints[i])['area_id'],
                          'description':
                              jsonDecode(queuedComplaints[i])['description'],
                          'latitude':
                              jsonDecode(queuedComplaints[i])['latitude'],
                          'longitude':
                              jsonDecode(queuedComplaints[i])['longitude'],
                          'attachments':
                              jsonDecode(queuedComplaints[i])['attachments'],
                        };

                        ///QA
                        Map<String, dynamic> qacomplaintData = {
                          'tagId': jsonDecode(queuedComplaints[i])['tagId'],
                          'area_id': jsonDecode(queuedComplaints[i])['area_id'],
                          'category_id':
                              jsonDecode(queuedComplaints[i])['category_id'],
                          'subcategory_id':
                              jsonDecode(queuedComplaints[i])['subcategory_id'],
                          'rating': jsonDecode(queuedComplaints[i])['rating'],
                          // 'description': jsonDecode(
                          //     queuedComplaints[i])['description'],
                          'latitude':
                              jsonDecode(queuedComplaints[i])['latitude'],
                          'longitude':
                              jsonDecode(queuedComplaints[i])['longitude'],
                          'attachments':
                              jsonDecode(queuedComplaints[i])['attachments'],
                        };

                        removeAndpostComplaintAndQAdata(
                            index: i,
                            complaint: complaintData,
                            qacomplaint: qacomplaintData);
                      }
                    } else {
                      funToast("No Internet Connectivity! ", appcolor);
                    }
                  },
                  backgroundColor: appcolor,
                  shape: CircleBorder(),
                  child: const Icon(
                    Icons.file_upload_outlined,
                    size: AppSize.s30,
                  ),
                )
              : Container()),
    );
  }
}
