import 'dart:convert';

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
import 'package:dha_ctt_app/view_model/view_models/complaint_state_model/complaint_list_detail_model.dart';
import 'package:dha_ctt_app/view_model/view_models/dashboard_model/dashboard_chat_model.dart';
import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:get/get.dart';
import 'package:progress_indicator/progress_indicator.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;

class TrackComplaints extends StatefulWidget {
  @override
  State<TrackComplaints> createState() => _TrackComplaintsState();
}

class _TrackComplaintsState extends State<TrackComplaints> {
  List<TrackComplaintItemModel> complaintListDetailModel = [];
  List<TrackComplaintItemModel> complaintListDetailModelMore = [];
  List<TrackComplaintItemModel> complaintListDetailModelUpdated = [];
  List<TrackComplaintItemModel> complaintListDetailModelUpdatedLoadMOre = [];
  List<String> ComplaintlistIds = [];

  List<DataItem> dashboardChatModel = [];
  List<DataItem> dashboardChatModelUpdated = [];
  bool _isLoading = false;
  String appBaseUrl = AppStrings.appBaseUrl;
  // List<StatusData> statusResponseDataList = [];
  int? complainStatusCounter = 0;
  double? progress;
  int? stattus1Count = 0;
  int? stattus2Count = 0;
  int? stattus3Count = 0;
  int? stattus4Count = 0;
  bool _isDownLoading = false;
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
  ScrollController _scrollController = ScrollController();
  bool _isMoreDataLoading = false;
  static String? trackComplaintpage;
  int? storedCountTotal;
  int activeButtonIndex = -1; // Initially, the first button is active

  @override
  void initState() {
    super.initState();
    // _isLoading = true;
    _isMoreDataLoading = true;
    _scrollController.addListener(_onScroll);
    refresh();
    getOwnComplaintListDataFromSharedPreferences();

    getDashboardChatFromSharedPreferences();

    //    getOthersComplaintListDataFromSharedPreferences();
    // getDashboardChatFromSharedPreferences();
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  void _onScroll() async {
    if (_scrollController.position.pixels ==
        _scrollController.position.maxScrollExtent) {
      setState(() {
        _isLoading = true;
        _isDownLoading = true;
      });
      print('test next api call =' + trackComplaintpage.toString());
      if (trackComplaintpage != null && trackComplaintpage != 'null') {
        String loadMoreApi = trackComplaintpage!.replaceAll('"', '');
        print('test 2 =' + loadMoreApi.replaceAll('"', ''));

        var connectivityResult = await (Connectivity().checkConnectivity());

        if (connectivityResult == ConnectivityResult.none) {
          funToast('Check Your Connection!', Colors.red);
          print("No internet connection");
          setState(() {
            _isLoading = false;
            _isDownLoading = false;
          });
        } else if (connectivityResult == ConnectivityResult.mobile) {
          print("Mobile data connection available");
          loadMoreTrackComlaintkList(
              loadMoreApi); // Load more data when reaching the end of the list
        } else if (connectivityResult == ConnectivityResult.wifi) {
          loadMoreTrackComlaintkList(
              loadMoreApi); // Load more data when reaching the end of the list
          print("WiFi connection available");
        }
      } else {
        setState(() {
          _isLoading = false;
          _isDownLoading = false;
        });
        funToast('All Complaints are loaded', appcolor);
        setState(() {
          _isScrolledToBottom = true;
        });
      }
    }
  }

  Future refresh() async {
    setState(() {
      storeTracComlaintkList();
      getOwnComplaintListDataFromSharedPreferences();
    });
  }

  //loadMoreTrackComlaintkList
  Future<void> loadMoreTrackComlaintkList(String apiLoadMore) async {
    if (!mounted) return; // Check if the widget is still mounted
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    final String token = prefs.getString('access_token') ?? '';
    print('URL = ' + apiLoadMore);

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
      

      print("Response : " + response.toString());
      // final response = await http.get(requestUri, headers: headers);

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

        trackComplaintpage = data['next'];
        storedCountTotal = data['count'];
        final List<dynamic> dataArray = data['results'];
        print("Total responce Responce load more: ${data}.");
        final List<TrackComplaintItemModel> complaint_list_model_new = dataArray
            .map((jsonData) => TrackComplaintItemModel.fromJson(jsonData))
            .toList();

        // final List<Map<String, dynamic>> serializedData = complaint_list_model
        //     .map((comlaintItemItem) => comlaintItemItem.toJson())
        //     .toList();
        complaintListDetailModelUpdatedLoadMOre.clear();
        if (apiLoadMore ==
            'http://58.65.172.155/complaint/api/own_complaint_list?page=2') {
          final String? trackComplaintListDataSerialzed =
              prefs.getString('trackComplaintListData');
          final List<dynamic> dataArray1 =
              jsonDecode(trackComplaintListDataSerialzed!);
          List<TrackComplaintItemModel> other_complaint_list_model1st =
              dataArray1
                  .map((json) => TrackComplaintItemModel.fromJson(json))
                  .toList();
          complaintListDetailModelUpdatedLoadMOre =
              // othersComplaintListDetailModel +
              other_complaint_list_model1st + complaint_list_model_new;
        } else {
          final String? trackComplaintListDataSerialzedMore =
              prefs.getString('trackComplaintListDataMore');
          try {
            final List<dynamic> dataArrayMore =
                jsonDecode(trackComplaintListDataSerialzedMore!);
            complaintListDetailModelMore = dataArrayMore
                .map((json) => TrackComplaintItemModel.fromJson(json))
                .toList();

            print(
                'Complaint List old Data size =  ${complaintListDetailModelMore.length} ');
            print(
                'Complaint List new Data size =  ${complaint_list_model_new.length} ');
            complaintListDetailModelUpdatedLoadMOre =
                // othersComplaintListDetailModel +
                complaintListDetailModelMore + complaint_list_model_new;
          } catch (e) {}
          try {
            setState(() {
              complaintListDetailModelUpdated =
                  complaint_list_model_new; // Update the status list
              ComplaintlistIds = complaintListDetailModelUpdated
                  .map((complaint) => complaint.uid)
                  .toList();
              complaintListDetailModelUpdatedLoadMOre =
                  // othersComplaintListDetailModel +
                  complaintListDetailModelMore + complaint_list_model_new;

              // ComplaintlistIds =
              //     complaintListDetailModel.map((complaint) => complaint.uid).toList();
              storeComplaintDetailsData(ComplaintlistIds);
              // Update the lists if needed

              print(
                  'Complaint List more Data size =  ${complaintListDetailModelUpdatedLoadMOre.length} ');
            });
          } catch (e) {
            print('error' + e.toString());

            complaintListDetailModelUpdated =
                complaint_list_model_new; // Update the status list
            ComplaintlistIds = complaintListDetailModelUpdated
                .map((complaint) => complaint.uid)
                .toList();
            complaintListDetailModelUpdatedLoadMOre =
                // othersComplaintListDetailModel +
                complaintListDetailModelMore + complaint_list_model_new;

            // ComplaintlistIds =
            //     complaintListDetailModel.map((complaint) => complaint.uid).toList();
            storeComplaintDetailsData(ComplaintlistIds);
            // Update the lists if needed
          }
        }
        print(
            'Complaint List more Data size =  ${complaintListDetailModelUpdatedLoadMOre.length} ');
        print('Next API SAVED FOR NEW CALL =  ${trackComplaintpage} ');
        print('Next API SAVED FOR privius CALL =  ${apiLoadMore} ');
        await prefs.setString(
            'trackComplaintpage', jsonEncode(trackComplaintpage));
        await prefs.setInt('countTotalTrack', storedCountTotal!);

        await prefs.setString('trackComplaintListDataMore',
            jsonEncode(complaintListDetailModelUpdatedLoadMOre));
        getOwnComplaintListDataFromSharedPreferences();
        // await prefs.setString('trackComplaintListData', jsonEncode(serializedData));
      } else {
        print(
            "API request Responce load more failed with status: ${response.statusCode}.");
      }
    } catch (e) {
      print('Exception occurred: $e');
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

  bool _isScrolledToBottom = false;

  void _scrollToTopOrBottom() {
    double targetOffset = _scrollController.offset + 100 * 20;
    double maxOffset = _scrollController.position.maxScrollExtent;
    // double maxOffset = _scrollController.offset + 100 * storedCountTotal!;

    if (_isScrolledToBottom) {
      // If scrolled to the bottom, change the icon and scroll to the top
      setState(() {
        _isScrolledToBottom = false;
      });
      _scrollController.animateTo(
        0,
        duration: Duration(milliseconds: 500),
        curve: Curves.easeInOut,
      );
    } else {
      // If not scrolled to the bottom, scroll down by 100 items
      setState(() {
        _isScrolledToBottom = false;
      });
      _scrollController.animateTo(
        targetOffset,
        duration: Duration(milliseconds: 500),
        curve: Curves.easeInOut,
      );
    }
  }

  void _scrollToTopOrBottom1() {
    if (_scrollController.offset >=
        _scrollController.position.maxScrollExtent) {
      // If already scrolled to the bottom, scroll to the top
      _scrollController.animateTo(
        0,
        duration: Duration(milliseconds: 500),
        curve: Curves.easeInOut,
      );
      setState(() {
        _isScrolledToBottom = false;
      });
    } else {
      // If not scrolled to the bottom, scroll to the bottom
      _scrollController.animateTo(
        _scrollController.position.maxScrollExtent,
        duration: Duration(milliseconds: 500),
        curve: Curves.easeInOut,
      );
    }
  }

// Function to retrieve status from SharedPreferences and populate the list
  Future<void> getOwnComplaintListDataFromSharedPreferences() async {
    if (!mounted) return; // Check if the widget is still mounted
    try {
      final SharedPreferences prefs = await SharedPreferences.getInstance();

      final String? trackComplaintListDataSerialzed1 =
          prefs.getString('trackComplaintListData');
      final String? trackComplaintListDataSerialzedAll =
          prefs.getString('trackComplaintListDataMore');
      String trackComplaintpagefirst =
          prefs.getString('trackComplaintpageFirst')!;
      String? trackComplaintpageMore = prefs.getString('trackComplaintpage');
      int countTotalOtherfirst = prefs.getInt('countTotalTrackFirst')!;
      int? countTotalOtherMOre = prefs.getInt('countTotalTrack');

      trackComplaintpage = trackComplaintpageMore ?? trackComplaintpagefirst;
      storedCountTotal = countTotalOtherfirst;
      0; // Default value is 0 if key doesn't exist
      print('new count = ' + countTotalOtherfirst.toString());
      print('old count = ' + countTotalOtherMOre.toString());
      String mergedData;

      if (trackComplaintpage!.replaceAll('"', '') ==
          'http://58.65.172.155/complaint/api/own_complaint_list?page=2') {
        // First, parse the JSON strings into lists

        final List<dynamic> firstList =
            jsonDecode(trackComplaintListDataSerialzed1 ?? "[]");

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
            jsonDecode(trackComplaintListDataSerialzed1 ?? "[]");

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

      if (mergedData.isNotEmpty) {
        final List<dynamic> dataArray = jsonDecode(mergedData);

        complaintListDetailModel = dataArray
            .map((json) => TrackComplaintItemModel.fromJson(json))
            .toList();

        ComplaintlistIds =
            complaintListDetailModel.map((complaint) => complaint.uid).toList();

        print('track list set = ' + complaintListDetailModel.length.toString());
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

        List<TrackComplaintItemModel> updatedDashboardList = [];

        complaintListDetailModel.forEach((status) {
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
  Future<void> getOwnComplaintListDataFromSharedPreferences1() async {
    try {
      // storeTracComlaintkList();
    } catch (e) {}
    try {
      final SharedPreferences prefs = await SharedPreferences.getInstance();
      // final String? trackComplaintListDataSerialzed =
      //     prefs.getString('trackComplaintListData');
      final String? trackComplaintListDataSerialzed =
          prefs.getString('trackComplaintListDataMore');

      trackComplaintpage = prefs.getString('trackComplaintpage');
      storedCountTotal = prefs.getInt('trackCountTotal') ??
          0; // Default value is 0 if key doesn't exist

      if (trackComplaintListDataSerialzed != null &&
          trackComplaintListDataSerialzed.isNotEmpty) {
        //    if (dashboardChatDataSerialzed.containsKey('status') &&
        //   response.data.containsKey('message')) {
        // var status = response.data['status'];
        // var message = response.data['message'];}
        print('stored data = ' + trackComplaintListDataSerialzed);
        final List<dynamic> dataArray =
            jsonDecode(trackComplaintListDataSerialzed);

        complaintListDetailModel = dataArray
            .map((json) => TrackComplaintItemModel.fromJson(json))
            .toList();

        ComplaintlistIds =
            complaintListDetailModel.map((complaint) => complaint.uid).toList();
        try {
          storeComplaintDetailsData(ComplaintlistIds);
          // Update the lists if needed
        } catch (e) {
          print('error saving comlaint details' + e.toString());
        }

        List<TrackComplaintItemModel> updatedDashboardList = [];

        complaintListDetailModel.forEach((status) {
          updatedDashboardList.add(status);
        });
        complaintListDetailModelUpdatedLoadMOre = updatedDashboardList;

        setState(() {
          _isDownLoading = false;
          complaintListDetailModelUpdated =
              updatedDashboardList; // Update the status list
          ComplaintlistIds = complaintListDetailModelUpdated
              .map((complaint) => complaint.uid)
              .toList();
          //   await  storeComplaintDetailsData(ComplaintlistIds);

          print('Complaint List Data =  $complaintListDetailModelUpdated ');
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
    if (filterName == 'null') {
      filterNameAndArg = Get.arguments[0];
    } else {
      filterNameAndArg = filterName;
    }

    if (activeButtonIndex == -1) {
      activeButtonIndex = Get.arguments[1];
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

// final fetchData = snapshot.data;
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

    // This controller will store the value of the search bar
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
                      "Track Complaint",
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
                    _isDownLoading
                        ? Container(
                            margin: EdgeInsets.only(
                                top: marginSet + 10,
                                bottom: marginSet,
                                left: marginLR + 15,
                                right: marginLR + 15),
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
                            margin: EdgeInsets.only(top: 5, right: 10),
                            alignment: Alignment.centerRight,
                            child: Text(
                              '${complaintListDetailModelUpdatedLoadMOre.length} out of ${storedCountTotal}',
                              style: TextStyle(
                                color: blackColor,
                                fontWeight: FontWeight.w800,
                              ),
                            ),
                          ),
                    Container(
                      margin: EdgeInsets.only(
                        bottom: 0,
                        top: 0,
                      ),

                      child:
                          // trackComplaintpage == null &&
                          trackComplaintpage == 'null' && filteredList.isEmpty
                              ? Center(
                                  child: Container(
                                    height: scHeight / 1.45,
                                    alignment: Alignment.center,
                                    child: Padding(
                                      padding: const EdgeInsets.all(2.0),
                                      child: Text(
                                        "No Complaints Available",
                                        style: TextStyle(
                                          color: Colors.red,
                                          fontWeight: FontWeight.w800,
                                          fontSize: dfFontSize,
                                        ),
                                      ),
                                    ),
                                  ), // You can replace this with your custom loader
                                )
                              : trackComplaintpage != null &&
                                      trackComplaintpage != 'null' &&
                                      filteredList.isEmpty
                                  ? Center(
                                      child: GestureDetector(
                                        onTap: () async {
                                          setState(() {
                                            _isLoading = true;
                                          });
                                          print('test next api call =' +
                                              trackComplaintpage.toString());
                                          if (trackComplaintpage != null &&
                                              trackComplaintpage != 'null') {
                                            String loadMoreApi =
                                                trackComplaintpage!
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
                                              loadMoreTrackComlaintkList(
                                                  loadMoreApi); // Load more data when reaching the end of the list
                                            } else if (connectivityResult ==
                                                ConnectivityResult.wifi) {
                                              loadMoreTrackComlaintkList(
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
                                          }
                                          setState(() {
                                            _isScrolledToBottom = true;
                                          });
                                          // funToast('test done', appcolor);
                                        },
                                        child: Container(
                                          height: scHeight / 1.45,
                                          alignment: Alignment.center,
                                          child: Padding(
                                              padding:
                                                  const EdgeInsets.all(5.0),
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
                                                        // ? 'asserts/gifs/loading.gif'
                                                        // : 'asserts/icons/load_more.png',
                                                        //  'asserts/icons/load_more.png',
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
                                  : Container(
                                      margin: EdgeInsets.symmetric(
                                          horizontal: marginLR),
                                      child: Column(
                                        children: [
                                          Stack(
                                            children: [
                                              Container(
                                                height: scHeight / 1.45,
                                                margin: EdgeInsets.only(
                                                    bottom: 5,
                                                    top: 20,
                                                    left: 0,
                                                    right: 0),
                                                child: ListView.builder(
                                                  scrollDirection:
                                                      Axis.vertical,
                                                  controller:
                                                      _scrollController, // Assign the ScrollController to the ListView
                                                  itemBuilder:
                                                      (BuildContext context,
                                                          int index) {
                                                    // Build your list items here
                                                    if (index <
                                                        filteredList.length) {
                                                      return TrackListWidget(
                                                        ComplaintlistIds:
                                                            ComplaintlistIds,
                                                        userId:
                                                            filteredList[index]
                                                                    .uid ??
                                                                'N/A',
                                                        trackDay: filteredList[
                                                                    index]
                                                                .createdOn ??
                                                            'N/A',
                                                        trackRefNo: filteredList[
                                                                    index]
                                                                .serialNumber ??
                                                            'N/A',
                                                        trackTime: filteredList[
                                                                    index]
                                                                .updatedOn ??
                                                            'N/A',
                                                        trackComplainStatus:
                                                            filteredList[index]
                                                                    .status ??
                                                                'N/A',
                                                        category:
                                                            filteredList[index]
                                                                    .category ??
                                                                'N/A',
                                                        subCategory: filteredList[
                                                                    index]
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
                                                        padding:
                                                            EdgeInsets.all(8.0),
                                                        child: Center(
                                                            child: // Show loading indicator when fetching more data
                                                                _isLoading
                                                                    ? Center(
                                                                        child:
                                                                            Row(
                                                                          children: [
                                                                            Image.asset(
                                                                              'asserts/gifs/loading.gif',
                                                                              width: scWidth / 3,
                                                                              // width: 120,
                                                                              // height: 120,
                                                                              // color: appcolor,
                                                                            ),
                                                                            Text('Loading More...')
                                                                          ],
                                                                        ),
                                                                      )
                                                                    : SizedBox() // Show nothing when not loading
                                                            ),
                                                      );
                                                    }
                                                  },
                                                  itemCount: filteredList
                                                          .length +
                                                      (_isLoading
                                                          ? 1
                                                          : 0), // Add one for the loading indicator

                                                  physics:
                                                      AlwaysScrollableScrollPhysics(),
                                                ),
                                              ),
                                              Positioned(
                                                bottom: 20,
                                                right: 20,
                                                child: ElevatedButton(
                                                  onPressed:
                                                      _scrollToTopOrBottom,
                                                  child: Icon(
                                                    _isScrolledToBottom
                                                        ? Icons
                                                            .keyboard_double_arrow_up
                                                        : Icons
                                                            .keyboard_double_arrow_down_sharp,
                                                    color: dfColor,
                                                  ),
                                                  style:
                                                      ElevatedButton.styleFrom(
                                                    backgroundColor: appcolor,
                                                    shape: CircleBorder(),
                                                    padding: EdgeInsets.all(20),
                                                  ),
                                                ),
                                              ),
                                            ],
                                          )
                                        ],
                                      ),
                                    ),

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
                    ),
                  ],
                ),
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
