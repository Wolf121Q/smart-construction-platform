import 'package:dha_ctt_app/view/screens/complaint/track_complaint/track_complaint.dart';
import 'package:dha_ctt_app/view/screens/dashboard/home.dart';
import 'package:dha_ctt_app/view/screens/login/login.dart';
import 'package:dha_ctt_app/view/screens/pending_task/pending_task.dart';
import 'package:dha_ctt_app/view/screens/splach/splach.dart';
import 'package:flutter/material.dart';

class Routes {
  static const String splashRoute = "/";
  static const String loginRoute = "/login";
  static const String homeRoute = "/home";
  static const String complaintRoute = "/complaint";
  static const String trackComplaintRoute = "/trackComplaint";
  // static const String complaintDetailRoute = "/complaintDetail";
  static const String qaComplaintRoute = "/qaComplaint";
  static const String pendingTaskRoute = "/pendingTask";
}

class RouteGenerator {
  static Route<dynamic> getRoute(RouteSettings routeSettings) {
    switch (routeSettings.name) {
      case Routes.splashRoute:
        return MaterialPageRoute(builder: (_) => Splach());
      case Routes.loginRoute:
        return MaterialPageRoute(builder: (_) => LogIn());
      case Routes.homeRoute:
        return MaterialPageRoute(builder: (_) => Home());
      // case Routes.complaintRoute:
      //   return MaterialPageRoute(builder: (_) => NewComplaint());
      case Routes.trackComplaintRoute:
        return MaterialPageRoute(builder: (_) => TrackComplaints());
      // case Routes.qaComplaintRoute:
      //   return MaterialPageRoute(builder: (_) => QACheckList());
      case Routes.pendingTaskRoute:
        return MaterialPageRoute(builder: (_) => PendingTask());

      default:
        return unDefinedRoute();
    }
  }

  static Route<dynamic> unDefinedRoute() {
    return MaterialPageRoute(
        builder: (_) => Scaffold(
              appBar: AppBar(title: Text("No Route Found")),
              body: Center(child: Text("No Route Found")),
            ));
  }
}
