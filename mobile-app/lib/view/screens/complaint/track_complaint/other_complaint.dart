import 'dart:convert';
import 'dart:isolate';

import 'package:connectivity/connectivity.dart';
import 'package:dha_ctt_app/constant.dart';
import 'package:dha_ctt_app/model/resources/string_manager.dart';
import 'package:dha_ctt_app/model/shared_preferences/share_pref_api_function.dart';
import 'package:dha_ctt_app/view/screens/dashboard/home.dart';
import 'package:dha_ctt_app/view/widgets/app_bar/custom_app_bar.dart';
import 'package:dha_ctt_app/view/screens/complaint/track_complaint/track_list_widget.dart';
import 'package:dha_ctt_app/view/widgets/dialogs/custom_dialog.dart';
import 'package:dha_ctt_app/view/widgets/dialogs/custom_toast.dart';
import 'package:dha_ctt_app/view_model/utils/color_widget.dart';
import 'package:dha_ctt_app/view_model/view_models/complaint_state_model/other_complaint_list_model.dart';
import 'package:dha_ctt_app/view_model/view_models/dashboard_model/dashboard_chat_model.dart';
import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:get/get.dart';
import 'package:progress_indicator/progress_indicator.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;

class OtherComplaints extends StatefulWidget {
  @override
  State<OtherComplaints> createState() => _OthersComplaintsState();
}

class _OthersComplaintsState extends State<OtherComplaints> {
  bool _isLoading = false;
  bool _isDownLoading = false;
  String appBaseUrl = AppStrings.appBaseUrl;
  int? complainStatusCounter = 0;
  List<DataItem> dashboardChatModel = [];
  List<DataItem> dashboardChatModelUpdated = [];
  List<OtherComplaintItemModel> othersComplaintListDetailModel = [];
  List<OtherComplaintItemModel> othersComplaintListDetailModelMore = [];

  List<OtherComplaintItemModel> othersComplaintListDetailModelUpdated = [];
  List<OtherComplaintItemModel> complaintListDetailModelUpdatedLoadMOre = [];
  List<String> ComplaintlistIds = [];
  ScrollController _scrollControllerOther = ScrollController();
  String? otherComplaintpage;
  int? storedCountTotal;
  int? stattus1Count = 0;
  int? stattus2Count = 0;
  int? stattus3Count = 0;
  int? stattus4Count = 0;

  String? stattus1Colour;
  String? stattus2Colour;
  String? stattus3Colour;
  String? stattus4Colour;

  String? stattus1Name;
  String? stattus2Name;
  String? stattus3Name;
  String? stattus4Name;
  String? filterNameAndArg;
  String filterName = 'null';
  bool _isScrolledToBottom = false;
  int activeButtonIndex = -1; // Initially, the first button is active

  @override
  void initState() {
    super.initState();
    // _isLoading = true;

    _scrollControllerOther.addListener(_onScroll);
    refresh();
    getOthersComplaintListDataFromSharedPreferences();
    getDashboardChatFromSharedPreferences();
  }

  @override
  void dispose() {
    _scrollControllerOther.dispose();

    super.dispose();
  }

  void _onScroll() async {
    if (!mounted) return; // Check if the widget is still mounted
    if (_scrollControllerOther.position.pixels ==
        _scrollControllerOther.position.maxScrollExtent) {
      setState(() {
        _isLoading = true;
      });
      print('test next api call =' + otherComplaintpage.toString());
      if (otherComplaintpage != "null" && otherComplaintpage != null) {
        String loadMoreApi = otherComplaintpage!.replaceAll('"', '');
        print('test 2 =' + loadMoreApi.replaceAll('"', ''));

        var connectivityResult = await (Connectivity().checkConnectivity());

        if (connectivityResult == ConnectivityResult.none) {
          funToast('Check Your Connection!', Colors.red);
          print("No internet connection");
          setState(() {
            _isLoading = false;
          });
        } else if (connectivityResult == ConnectivityResult.mobile) {
          print("Mobile data connection available");
          loadMoreotherComlaintkList(
              loadMoreApi); // Load more data when reaching the end of the list
        } else if (connectivityResult == ConnectivityResult.wifi) {
          loadMoreotherComlaintkList(
              loadMoreApi); // Load more data when reaching the end of the list
          print("WiFi connection available");
        }
      } else {
        setState(() {
          _isLoading = false;
        });
        funToast('All Complaints are loaded', appcolor);
        setState(() {
          _isScrolledToBottom = true;
          _isDownLoading = false;
        });
      }
    }
  }

  void _scrollToTopOrBottom() {
    double targetOffset = _scrollControllerOther.offset + 100 * 100;
    // double maxOffset = _scrollControllerOther.position.maxScrollExtent;
    double maxOffset = _scrollControllerOther.offset + 100 * storedCountTotal!;
    if (_isScrolledToBottom) {
      // If scrolled to the bottom, change the icon and scroll to the top
      setState(() {
        _isScrolledToBottom = false;
      });
      _scrollControllerOther.animateTo(
        0,
        duration: Duration(milliseconds: 500),
        curve: Curves.easeInOut,
      );
    } else {
      // If not scrolled to the bottom, scroll down by 100 items
      setState(() {
        _isScrolledToBottom = false;
      });
      _scrollControllerOther.animateTo(
        targetOffset,
        duration: Duration(milliseconds: 500),
        curve: Curves.easeInOut,
      );
    }
  }

  void _scrollToTopOrBottom1() {
    if (_scrollControllerOther.offset >=
        _scrollControllerOther.position.maxScrollExtent) {
      // If already scrolled to the bottom, scroll to the top
      _scrollControllerOther.animateTo(
        0,
        duration: Duration(milliseconds: 500),
        curve: Curves.easeInOut,
      );
      setState(() {
        _isScrolledToBottom = false;
      });
    } else {
      // If not scrolled to the bottom, scroll to the bottom
      _scrollControllerOther.animateTo(
        _scrollControllerOther.position.maxScrollExtent,
        duration: Duration(milliseconds: 500),
        curve: Curves.easeInOut,
      );
    }
  }

  //loadMoreTracComlaintkList
  Future<void> loadMoreotherComlaintkList(String apiLoadMore) async {
    if (!mounted) return; // Check if the widget is still mounted
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    final String token = prefs.getString('access_token') ?? '';

    Map<String, String> headers = {
      'Authorization': 'Bearer $token',
    };
    Uri requestUri = Uri.parse(apiLoadMore);
    // Uri requestUri = Uri.parse(apiLoadMore);

    // Modify the URI to add the port
   // Uri requestUriPort = requestUri.replace(port: 54327);

    try {
     // final response = await http.get(requestUriPort, headers: headers);

       final response = await http.get(requestUri, headers: headers);

      // final response = await http.get(Uri.parse(apiLoadMore), headers: headers);

      print("Responce load more  : " + response.toString());

      if (response.statusCode == 200) {
        //  final Map<String, dynamic> responseData = json.decode(response.body);
        try {
          setState(() {
            _isLoading = false;
          });
        } catch (e) {
          _isLoading = false;
          print('error' + e.toString());
        }

        // return ComplaintListDetailModel.fromJson(responseData);
        // final jsonData = json.decode(response.body);
        final Map<String, dynamic> data = jsonDecode(response.body);

        otherComplaintpage = data['next'];
        storedCountTotal = data['count'];
        final List<dynamic> dataArray = data['results'];
        print("Total responce Responce load more: ${data}.");
        final List<OtherComplaintItemModel> complaint_list_model_new = dataArray
            .map((jsonData) => OtherComplaintItemModel.fromJson(jsonData))
            .toList();

        // final List<Map<String, dynamic>> serializedData = complaint_list_model
        //     .map((comlaintItemItem) => comlaintItemItem.toJson())
        //     .toList();
        complaintListDetailModelUpdatedLoadMOre.clear();
        if (apiLoadMore ==
            'http://58.65.172.155/complaint/api/complaint_list?page=2') {
          final String? trackComplaintListDataSerialzed =
              prefs.getString('othersComplaintListData');
          final List<dynamic> dataArray1 =
              jsonDecode(trackComplaintListDataSerialzed!);
          List<OtherComplaintItemModel> other_complaint_list_model1st =
              dataArray1
                  .map((json) => OtherComplaintItemModel.fromJson(json))
                  .toList();
          complaintListDetailModelUpdatedLoadMOre =
              // othersComplaintListDetailModel +
              other_complaint_list_model1st + complaint_list_model_new;
        } else {
          final String? trackComplaintListDataSerialzedMore =
              prefs.getString('othersComplaintListDataMore');
          try {
            final List<dynamic> dataArrayMore =
                jsonDecode(trackComplaintListDataSerialzedMore!);
            othersComplaintListDetailModelMore = dataArrayMore
                .map((json) => OtherComplaintItemModel.fromJson(json))
                .toList();

            print(
                'Complaint List old Data size =  ${othersComplaintListDetailModelMore.length} ');
            print(
                'Complaint List new Data size =  ${complaint_list_model_new.length} ');
            complaintListDetailModelUpdatedLoadMOre =
                // othersComplaintListDetailModel +
                othersComplaintListDetailModelMore + complaint_list_model_new;
          } catch (e) {}
          try {
            setState(() {
              othersComplaintListDetailModelUpdated =
                  complaint_list_model_new; // Update the status list
              ComplaintlistIds = othersComplaintListDetailModelUpdated
                  .map((complaint) => complaint.uid)
                  .toList();
              complaintListDetailModelUpdatedLoadMOre =
                  // othersComplaintListDetailModel +
                  othersComplaintListDetailModelMore + complaint_list_model_new;

              // ComplaintlistIds =
              //     complaintListDetailModel.map((complaint) => complaint.uid).toList();
              storeComplaintDetailsData(ComplaintlistIds);
              // Update the lists if needed

              print(
                  'Complaint List more Data size =  ${complaintListDetailModelUpdatedLoadMOre.length} ');
            });
          } catch (e) {
            print('error' + e.toString());

            othersComplaintListDetailModelUpdated =
                complaint_list_model_new; // Update the status list
            ComplaintlistIds = othersComplaintListDetailModelUpdated
                .map((complaint) => complaint.uid)
                .toList();
            complaintListDetailModelUpdatedLoadMOre =
                // othersComplaintListDetailModel +
                othersComplaintListDetailModelMore + complaint_list_model_new;

            // ComplaintlistIds =
            //     complaintListDetailModel.map((complaint) => complaint.uid).toList();
            storeComplaintDetailsData(ComplaintlistIds);
            // Update the lists if needed
          }
        }
        print(
            'Complaint List more Data size =  ${complaintListDetailModelUpdatedLoadMOre.length} ');
        print('Next API SAVED FOR NEW CALL =  ${otherComplaintpage} ');
        print('Next API SAVED FOR privius CALL =  ${apiLoadMore} ');
        await prefs.setString(
            'otherComplaintpage', jsonEncode(otherComplaintpage));
        await prefs.setInt('countTotalOther', storedCountTotal!);

        await prefs.setString('othersComplaintListDataMore',
            jsonEncode(complaintListDetailModelUpdatedLoadMOre));
        getOthersComplaintListDataFromSharedPreferences();
        // await prefs.setString('trackComplaintListData', jsonEncode(serializedData));
      } else {
        print(
            "API request Responce load more failed with status: ${response.statusCode}.");
      }
    } catch (e) {
      print('Exception occurred: $e');
    }
  }

  ///refresh
  Future refresh() async {
    if (!mounted) return; // Check if the widget is still mounted
    setState(() {
      storeOthersComlaintkList();
      getOthersComplaintListDataFromSharedPreferences();
    });
  }

// Function to retrieve status from SharedPreferences and populate the list
  Future<void> getOthersComplaintListDataFromSharedPreferences() async {
    if (!mounted) return; // Check if the widget is still mounted
    try {
      final SharedPreferences prefs = await SharedPreferences.getInstance();

      final String? otherComplaintListDataSerialzed1 =
          prefs.getString('othersComplaintListData');
      final String? trackComplaintListDataSerialzedAll =
          prefs.getString('othersComplaintListDataMore');
      String trackComplaintpagefirst =
          prefs.getString('otherComplaintpageFirst')!;
      String? otherComplaintpageMore = prefs.getString('otherComplaintpage');
      int countTotalOtherfirst = prefs.getInt('countTotalOtherFirst')!;
      int? countTotalOtherMOre = prefs.getInt('countTotalOther');

      otherComplaintpage = otherComplaintpageMore ?? trackComplaintpagefirst;
      storedCountTotal = countTotalOtherfirst;
      0; // Default value is 0 if key doesn't exist

      String mergedData;
      if (otherComplaintpage!.replaceAll('"', '') ==
          'http://58.65.172.155/complaint/api/complaint_list?page=2') {
        // First, parse the JSON strings into lists

        final List<dynamic> firstList =
            jsonDecode(otherComplaintListDataSerialzed1 ?? "[]");

// Then, concatenate the lists
        final List<dynamic> mergedList = firstList;
        mergedData = jsonEncode(mergedList);
      } else {
        final List<dynamic> secondList =
            jsonDecode(trackComplaintListDataSerialzedAll ?? "[]");

// Then, concatenate the lists
        final List<dynamic> mergedList = secondList;
        mergedData = jsonEncode(mergedList);
      }
      if (countTotalOtherMOre != countTotalOtherfirst) {
        print('New data available');

        // Deserialize the old data from the string into a Dart list
        List<dynamic> oldList = jsonDecode(mergedData ?? "[]");

        // Deserialize the new data from the string into a Dart list
        List<dynamic> newList =
            jsonDecode(otherComplaintListDataSerialzed1 ?? "[]");

        // Create a set to store unique serial numbers
        Set<String> serialNumbers =
            Set.from(oldList.map((item) => item['serial_number']));

        // Filter out items with duplicate serial numbers from the new list
        List<dynamic> uniqueItems = newList
            .where((item) => !serialNumbers.contains(item['serial_number']))
            .toList();

        // Concatenate the old list with the list of unique items
        List<dynamic> mergedList = [...oldList, ...uniqueItems];

        // Serialize the merged list back into a string
        mergedData = jsonEncode(mergedList);
      }

// Check if both strings are not null before merging

      print('marge data' + otherComplaintListDataSerialzed1!);
      if (mergedData.isNotEmpty) {
        final List<dynamic> dataArray = jsonDecode(mergedData);

        othersComplaintListDetailModel = dataArray
            .map((json) => OtherComplaintItemModel.fromJson(json))
            .toList();

        ComplaintlistIds = othersComplaintListDetailModel
            .map((complaint) => complaint.uid)
            .toList();
        setState(() {
          _isLoading = false;
        });
        try {
          storeComplaintDetailsData(ComplaintlistIds);
          // Update the lists if needed
        } catch (e) {
          print('error saving comlaint details' + e.toString());
        }
        // storeComplaintDetailsData(ComplaintlistIds);
        // // Update the lists if needed

        List<OtherComplaintItemModel> updatedDashboardList = [];

        othersComplaintListDetailModel.forEach((status) {
          updatedDashboardList.add(status);
        });

        complaintListDetailModelUpdatedLoadMOre = updatedDashboardList;

        // setState(() {
        //   othersComplaintListDetailModelUpdated =
        //       updatedDashboardList; // Update the status list
        //   _isLoading = false;
        //   ComplaintlistIds = othersComplaintListDetailModelUpdated
        //       .map((complaint) => complaint.uid)
        //       .toList();

        //   storeComplaintDetailsData(ComplaintlistIds);
        //   print('Data =  $othersComplaintListDetailModelUpdated ');
        // });
      } else {
        print('No Dashboard data found in SharedPreferences.');
      }
    } catch (e) {
      print('Error retrieving Dashboard data from SharedPreferences: $e');
    }
  }

  // Function to retrieve status from SharedPreferences and populate the list
  Future<void> getDashboardChatFromSharedPreferences() async {
    if (!mounted) return; // Check if the widget is still mounted
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
          dashboardChatModelUpdated =
              updatedDashboardList; // Update the status list
        });
      } else {
        print('No Dashboard data found in SharedPreferences.');
      }
    } catch (e) {
      print('Error retrieving Dashboard data from SharedPreferences: $e');
    }
  }

// Define a function to handle loading more complaints
  void loadMoreComplaints() async {
    if (!mounted) return; // Check if the widget is still mounted
    setState(() {
      _isLoading = true;
      _isDownLoading = true;
    });
    if (otherComplaintpage != null && otherComplaintpage != 'null') {
      funToast('Download Started', appcolor);
    } else {
      funToast('Something went wrong', Colors.red);
    }

    // Continuously fetch complaints until loadMoreApi is null
    while (otherComplaintpage != null && otherComplaintpage != 'null') {
      var connectivityResult = await (Connectivity().checkConnectivity());

      if (connectivityResult == ConnectivityResult.none) {
        funToast('Check Your Connection!', Colors.red);
        print("No internet connection");
        setState(() {
          _isLoading = false;
        });
        break; // Exit the loop if there's no internet connection
      } else {
        // Make API call to fetch complaints
        try {
          // loadMoreotherComlaintkListcatch(
          //     otherComplaintpage!.replaceAll('"', ''));
          loadMoreotherComlaintkList(otherComplaintpage!.replaceAll('"', ''));
        } catch (e) {
          // loadMoreotherComlaintkListcatch(
          //     otherComplaintpage!.replaceAll('"', ''));
        }

        // Wait for a certain time before sending the next request
        // Adjust the waiting time based on your requirements
        await Future.delayed(Duration(seconds: 1)); // Example: 1 second
      }
    }

    setState(() {
      _isLoading = false;
      _isDownLoading = false;
    });

    funToast('Your Up To Date Data is already Downloaded', appcolor);
  }

// Define the function that initiates the loading of complaints
  void initiateComplaintLoading() {
    Navigator.pop(context); // Dismiss the dialog
    loadMoreComplaintsAll();
  }

  void loadMoreComplaintsAll() {
    // Start the background isolate
    ReceivePort receivePort = ReceivePort();
    Isolate.spawn(_backgroundTask, receivePort.sendPort);
    // Set loading state
    setState(() {
      _isLoading = true;
      _isDownLoading = true;
    });
    // Show initial toast
    if (otherComplaintpage != null && otherComplaintpage != 'null') {
      funToast('Download Started', appcolor);
    } else {
      funToast('Something went wrong', Colors.red);
    }
  }

  void _backgroundTask(SendPort sendPort) async {
    // Continuously fetch complaints until loadMoreApi is null
    while (otherComplaintpage != null && otherComplaintpage != 'null') {
      var connectivityResult = await (Connectivity().checkConnectivity());
      if (connectivityResult == ConnectivityResult.none) {
        // Show toast for no internet connection
        funToast('Check Your Connection!', Colors.red);
        print("No internet connection");
        break; // Exit the loop if there's no internet connection
      } else {
        // Make API call to fetch complaints
        try {
          loadMoreotherComlaintkList(otherComplaintpage!.replaceAll('"', ''));
        } catch (e) {
          // Handle errors if any
        }
        // Wait for a certain time before sending the next request
        // Adjust the waiting time based on your requirements
        await Future.delayed(Duration(seconds: 1)); // Example: 1 second
      }
    }
    // Send a message to the main isolate to update the UI
    sendPort.send(true);
  }

  @override
  Widget build(BuildContext context) {
    // This controller will store the value of the search bar

    if (filterName == 'null') {
      filterNameAndArg = Get.arguments[0];
    } else {
      filterNameAndArg = filterName;
    }

    if (activeButtonIndex == -1) {
      activeButtonIndex = Get.arguments[1];
    }
    int len = dashboardChatModelUpdated.length;

    for (int i = 0; i < len; i++) {
      if (dashboardChatModelUpdated[i].code == "Total") {
        stattus1Name = dashboardChatModelUpdated[i].name;
        stattus1Colour = appcolorHex;
        stattus1Count = dashboardChatModelUpdated[i].total;
      } else if (dashboardChatModelUpdated[i].code ==
          "system_status_complaints_resolved") {
        stattus2Name = dashboardChatModelUpdated[i].name;
        stattus2Colour = dashboardChatModelUpdated[i].color;
        stattus2Count = dashboardChatModelUpdated[i].total;
      } else if (dashboardChatModelUpdated[i].code ==
          "system_status_complaints_in_process") {
        stattus3Name = dashboardChatModelUpdated[i].name;
        stattus3Colour = dashboardChatModelUpdated[i].color;
        stattus3Count = dashboardChatModelUpdated[i].total;
      } else if (dashboardChatModelUpdated[i].code ==
          "system_status_complaints_Reopened") {
        stattus4Name = dashboardChatModelUpdated[i].name;
        stattus4Colour = dashboardChatModelUpdated[i].color;
        stattus4Count = dashboardChatModelUpdated[i].total;
      }
    }

    final filteredList;
    if (filterNameAndArg == "Total") {
      filteredList = complaintListDetailModelUpdatedLoadMOre;
    } else {
      // Filter the list based on the "status" field
      filteredList = complaintListDetailModelUpdatedLoadMOre
          .where((item) => item.status == filterNameAndArg)
          .toList();
    }

    final TextEditingController _searchController = TextEditingController();
    double scWidth = MediaQuery.of(context).size.width;
    double scHeight = MediaQuery.of(context).size.height;
    return RefreshIndicator(
      onRefresh: refresh,
      child: Scaffold(
        appBar: CustomAppBar(
            navFunction: () {
              Navigator.pushAndRemoveUntil(
                context,
                MaterialPageRoute(builder: (context) => const Home()),
                (Route<dynamic> route) =>
                    false, // This ensures all previous routes are removed
              );
            },
            lastIcon: Icons.info_outline,
            infoFunction: () {
              CustomDialog(context);
            }),
        // },
        // lastIcon: Icons.settings,
        // infoFunction: () {
        //   downloadAllComplaintDialog(context,
        //       fun: initiateComplaintLoading, isDownLoading: _isDownLoading);
        // }),
        body: Container(
          color: drakGreyColor,
          child: Column(
            mainAxisSize: MainAxisSize.max,
            // mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: <Widget>[
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
                      "Other Complaint",
                      style: TextStyle(
                        color: dfColor,
                        fontWeight: FontWeight.w600,
                        fontSize: dfFontSize - 2,
                      ),
                    ),
                  ),
                ),
              ),

              Container(
                margin: EdgeInsets.symmetric(horizontal: 0),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: [
                    buildButton(0, stattus1Name ?? '....',
                        stattus1Colour ?? appcolorHex, lightappcolor),
                    buildButton(1, stattus2Name ?? '....',
                        stattus2Colour ?? appcolorHex, lightappcolor),
                    buildButton(2, stattus3Name ?? '....',
                        stattus3Colour ?? appcolorHex, lightappcolor),
                    buildButton(3, stattus4Name ?? '....',
                        stattus4Colour ?? appcolorHex, lightappcolor),
                  ],
                ),
              ),

              Expanded(
                flex: 11,
                child: Column(
                  children: [
                    Container(
                      margin: EdgeInsets.symmetric(horizontal: marginLR),
                      child: Column(
                        children: [
                          _isDownLoading
                              ? Container(
                                  margin: EdgeInsets.only(
                                      top: marginSet + 10,
                                      bottom: marginSet,
                                      left: marginLR,
                                      right: marginLR),
                                  child: BarProgress(
                                    percentage:
                                        complaintListDetailModelUpdatedLoadMOre
                                                .length /
                                            storedCountTotal! *
                                            100,
                                    backColor: Colors.grey,
                                    // gradient: LinearGradient(
                                    //     colors: [Colors.blue, Colors.red]),
                                    color: appcolor,
                                    showPercentage: true,
                                    textStyle:
                                        TextStyle(color: dfColor, fontSize: 15),
                                    stroke: 20,
                                    round: true,
                                  ),
                                )
                              : Container(
                                  margin: EdgeInsets.only(
                                      top: 5, right: 15, bottom: 0),
                                  alignment: Alignment.centerRight,
                                  child: Text(
                                    '${complaintListDetailModelUpdatedLoadMOre.length} out of ${storedCountTotal}',
                                    style: TextStyle(
                                      color: blackColor,
                                      fontWeight: FontWeight.w800,
                                    ),
                                  ),
                                ),
                          otherComplaintpage == null ||
                                  otherComplaintpage == 'null' &&
                                      filteredList.isEmpty
                              ? Center(
                                  child:
                                      //  CircularProgressIndicator(), // You can replace this with your custom loader
                                      Container(
                                    height: scHeight / 1.45,
                                    alignment: Alignment.center,
                                    child: Padding(
                                      padding: const EdgeInsets.all(2.0),
                                      child: Text(
                                        "No Complaint Data Available",
                                        style: TextStyle(
                                          color: Colors.red,
                                          fontWeight: FontWeight.w800,
                                          fontSize: dfFontSize,
                                        ),
                                      ),
                                    ),
                                  ), // You can replace this with your custom loader
                                )
                              : otherComplaintpage != null &&
                                      otherComplaintpage != 'null' &&
                                      filteredList.isEmpty
                                  ? Center(
                                      child: GestureDetector(
                                        onTap: () async {
                                          if (!mounted)
                                            return; // Check if the widget is still mounted
                                          setState(() {
                                            _isLoading = true;
                                          });
                                          print('test next api call =' +
                                              otherComplaintpage.toString());
                                          if (otherComplaintpage != null &&
                                              otherComplaintpage != 'null') {
                                            String loadMoreApi =
                                                otherComplaintpage!
                                                    .replaceAll('"', '');
                                            print('test 2 =' +
                                                loadMoreApi.replaceAll(
                                                    '"', ''));

                                            var connectivityResult =
                                                await (Connectivity()
                                                    .checkConnectivity());

                                            if (connectivityResult ==
                                                ConnectivityResult.none) {
                                              funToast('Check Your Connection!',
                                                  Colors.red);
                                              print("No internet connection");
                                              setState(() {
                                                _isLoading = false;
                                              });
                                            } else if (connectivityResult ==
                                                ConnectivityResult.mobile) {
                                              print(
                                                  "Mobile data connection available");
                                              loadMoreotherComlaintkList(
                                                  loadMoreApi); // Load more data when reaching the end of the list
                                            } else if (connectivityResult ==
                                                ConnectivityResult.wifi) {
                                              loadMoreotherComlaintkList(
                                                  loadMoreApi); // Load more data when reaching the end of the list
                                              print(
                                                  "WiFi connection available");
                                            }
                                          } else {
                                            setState(() {
                                              _isLoading = false;
                                            });
                                            funToast(
                                                'All Complaints are loaded',
                                                appcolor);
                                            setState(() {
                                              _isScrolledToBottom = true;
                                            });
                                          }
                                          // funToast('test done', appcolor);
                                        },
                                        child: Container(
                                          height: scHeight / 1.45,
                                          alignment: Alignment.center,
                                          child: Padding(
                                              padding:
                                                  const EdgeInsets.all(1.0),
                                              child: Container(
                                                width: scWidth / 2.5,
                                                // decoration: BoxDecoration(
                                                //     color: appcolor,
                                                //     borderRadius:
                                                //         BorderRadius.circular(15)),
                                                child: Row(
                                                  mainAxisAlignment:
                                                      MainAxisAlignment.center,
                                                  children: [
                                                    // Text(
                                                    //   'Load More',
                                                    //   style: TextStyle(
                                                    //       fontSize: scWidth / 25,
                                                    //       color: dfColor,
                                                    //       fontWeight:
                                                    //           FontWeight.w600),
                                                    // ),
                                                    Padding(
                                                      padding:
                                                          const EdgeInsets.all(
                                                              8.0),
                                                      child: Image.asset(
                                                        _isLoading
                                                            ? 'asserts/gifs/loading.gif'
                                                            : 'asserts/icons/load_more.png',
                                                        // 'asserts/icons/load_more.png',
                                                        width: scWidth / 4,
                                                        fit: BoxFit.fill,
                                                        // width: 120,
                                                        // height: 120,
                                                        // color: appcolor,
                                                      ),
                                                    ),
                                                  ],
                                                ),
                                              )),
                                        ),
                                      ), // You can replace this with your custom loader
                                    )
                                  : Stack(
                                      children: [
                                        Container(
                                          height: scHeight / 1.45,
                                          margin: EdgeInsets.only(
                                              bottom: 5,
                                              top: 5,
                                              left: 0,
                                              right: 0),
                                          child: ListView.builder(
                                            scrollDirection: Axis.vertical,
                                            controller:
                                                _scrollControllerOther, // Assign the ScrollController to the ListView
                                            itemBuilder: (BuildContext context,
                                                int index) {
                                              if (index < filteredList.length) {
                                                return TrackListWidget(
                                                  ComplaintlistIds:
                                                      ComplaintlistIds,
                                                  userId:
                                                      filteredList[index].uid ??
                                                          'N/A',
                                                  trackDay: filteredList[index]
                                                          .createdOn ??
                                                      'N/A',
                                                  trackRefNo:
                                                      filteredList[index]
                                                              .serialNumber ??
                                                          'N/A',
                                                  trackTime: filteredList[index]
                                                          .updatedOn ??
                                                      'N/A',
                                                  trackComplainStatus:
                                                      filteredList[index]
                                                              .status ??
                                                          'N/A',
                                                  category: filteredList[index]
                                                          .category ??
                                                      'N/A',
                                                  subCategory:
                                                      filteredList[index]
                                                              .subcategory ??
                                                          'N/A',
                                                  colorComplait:
                                                      HexColor.fromHex(
                                                              filteredList[
                                                                      index]
                                                                  .color) ??
                                                          appcolor,
                                                  index: index + 1,
                                                );
                                              } else {
                                                // Show loading indicator when fetching more data
                                                return Padding(
                                                  padding: EdgeInsets.all(8.0),
                                                  child: Center(
                                                      child: // Show loading indicator when fetching more data
                                                          _isLoading
                                                              ? Center(
                                                                  child: Row(
                                                                    children: [
                                                                      Image
                                                                          .asset(
                                                                        'asserts/gifs/loading.gif',

                                                                        //  'asserts/gifs/loading.gif',
                                                                        width:
                                                                            scWidth /
                                                                                3,
                                                                        // width: 120,
                                                                        // height: 120,
                                                                        // color: appcolor,
                                                                      ),
                                                                      Text(
                                                                          'Loading More...')
                                                                    ],
                                                                  ),
                                                                )
                                                              : SizedBox() // Show nothing when not loading
                                                      ),
                                                );
                                              }
                                            },
                                            itemCount: filteredList.length +
                                                (_isLoading
                                                    ? 1
                                                    : 0), // Add one for the loading indicator

                                            physics:
                                                AlwaysScrollableScrollPhysics(), // Add this line
                                          ),
                                        ),
                                        // Button to trigger scrolling
                                        Positioned(
                                          bottom: 20,
                                          right: 20,
                                          child: ElevatedButton(
                                            onPressed: _scrollToTopOrBottom,
                                            child: Icon(
                                              _isScrolledToBottom
                                                  ? Icons
                                                      .keyboard_double_arrow_up
                                                  : Icons
                                                      .keyboard_double_arrow_down_sharp,
                                              color: dfColor,
                                            ),
                                            style: ElevatedButton.styleFrom(
                                              backgroundColor: appcolor,
                                              shape: CircleBorder(),
                                              padding: EdgeInsets.all(20),
                                            ),
                                          ),
                                        ),
                                      ],
                                    ),
                        ],
                      ),
                    ),
                  ],
                ),

                // child:

                // Container(
                //   margin: EdgeInsets.only(
                //       bottom: 5, top: 20, left: marginLR, right: marginLR),
                //   child: ListView.builder(
                //     scrollDirection: Axis.vertical,
                //     itemBuilder: (BuildContext context, int index) {
                //       return TrackListWidget(
                //         ComplaintlistIds: ComplaintlistIds,
                //         userId: filteredList[index].uid ?? 'N/A',
                //         trackDay: filteredList[index].createdOn ?? 'N/A',
                //         trackRefNo: filteredList[index].serialNumber ?? 'N/A',
                //         trackTime: filteredList[index].updatedOn ?? 'N/A',
                //         trackComplainStatus:
                //             filteredList[index].status ?? 'N/A',
                //         category: filteredList[index].category ?? 'N/A',
                //         subCategory: filteredList[index].subcategory ?? 'N/A',
                //         colorComplait:
                //             HexColor.fromHex(filteredList[index].color) ??
                //                 appcolor,
                //       );
                //     },
                //     itemCount: filteredList.length,
                //   ),
                // ),
              ),

              //     }
              //   },
              // )
            ],
          ),
        ),
      ),
    );
  }

  ElevatedButton buildButton(
      int index, String label, String activeColor, inactiveColor) {
    return ElevatedButton(
      onLongPress: () {
        Fluttertoast.showToast(
          msg: label,
          toastLength: Toast.LENGTH_SHORT, // or Toast.LENGTH_LONG
          gravity: ToastGravity.BOTTOM, // You can change the position
          timeInSecForIosWeb: 1, // time in seconds
          backgroundColor: Colors.grey,
          textColor: Colors.white,
          fontSize: 16.0,
        );
      },
      onPressed: () {
        // Set the active button index when pressed
        setState(() {
          activeButtonIndex = index;
          filterName = label;
        });
      },
      style: ElevatedButton.styleFrom(
        //  padding: EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0), // Custom padding
        backgroundColor: index == activeButtonIndex
            ? HexColor.fromHex(activeColor) // Custom color for active button
            : inactiveColor, // Custom color for inactive buttons
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(roundBtn - 5), // Custom radius
        ),
      ),
      child: Text(label,
          style: TextStyle(
              fontSize: index == activeButtonIndex
                  ? smFontSize - 7 // Custom color for active button
                  : smFontSize - 8,
              fontWeight: index == activeButtonIndex
                  ? FontWeight.w900 // Custom color for active button
                  : FontWeight.bold,
              color: Colors.white)),
    );
  }
}
