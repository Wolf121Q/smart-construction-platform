class AppStrings {
//----------------------------------Api Constants------------
  // static const String appBaseUrl = "https://ctt.dhai-r.com.pk/"; //real database
  // static const String appBaseUrl =
  //     "http://192.168.150.125:8000/"; //local database
  static const String appBaseUrl = "http://65.108.212.69/"; //local database

  // static const String appBaseUrl = "https://ctt.dhai-r.com.pk/"; //live database
  // static const String appBaseUrlimage =
  //     "https://ctt.dhai-r.com.pk"; //live database
  static const String appBaseUrlimage = "http://65.108.212.69"; //local database
  static const String LOGIN_URI = "complaint/api/login";
  //     "http://65.21.153.247:8080"; //local database
  // static const String LOGIN_URI = "complaint/api/login";

  //--------TRACK COMPLAINT
  static const String OWN_COMPLAINT_LIST = "complaint/api/own_complaint_list";

  //--------Other COMPLAINT
  static const String OTHER_COMPLAINT_LIST = "complaint/api/complaint_list";

  // ------------- Compliant Details
  static const String COMPLAINT_ACTION_LIST_DETAILS =
      "complaint/api/complaint/";
  static const String COMPLAINT_ACTION_COMMENTS_DETAILS =
      "complaint/api/complaint_action_comments/";
  static const String COMPLAINT_ACTION_COMMENTS_IMAGE_DETAILS =
      "complaint/api/complaint_action_files/";

//--------UPDATE COMPLAINT
  static const String UPDATE_COMPLAINT_LIST = "complaint/api/update_complaint";

  //----------Dashboard
  static const String DASHBOARD_CHART_DATA = "complaint/api/dashboard_api";

  //----------ComplaintStatuses
  static const String COMPLAINT_STATUSES_DATA =
      "complaint/api/complaint_statuses";

//----------New Complaint
  static const String NEW_COMPLAINT = "complaint/api/insert_complaint";

//----------QA Complaint
  static const String QA_CHECKLIST = "complaint/api/insert_qa_checklist";

//----------GET Category
  static const String GET_CATEGORY = "complaint/api/categories";

  //----------QA GET Category
  static const String QA_GET_CATEGORY = "complaint/api/qa_checklist_categories";

  //----------QA Rating
  static const String QA_GET_RATING =
      "complaint/api/qa_checklist_rating_choices";

//----------complaint statuses
  static const String COMPLAINT_STATUS = "complaint/api/complaint_statuses";

  //----------Area
  static const String AREA_HIERARCHY = "complaint/api/area_hierarchy";
}

class LocalDBStrings {
  static const String login_user = "login_user";
  static const String dashboard_chart = "dashboard_chart";
}
