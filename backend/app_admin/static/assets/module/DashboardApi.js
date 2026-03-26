var DashboardApi = (function () {
    /*
     * Alias of this
     * @private
     */
    var self = {};
    /**
     * Sort an autocompletion result array with insensitivity to the case,
     * using the 1st elements (a[0] and b[0]) to process comparison
     * @public
     * @param {array} a
     * @param {array} b
     * @return {undefined}
     */

    //  admin/member/payment_schedule


    self.TaskDetailWindow = function(id='')
    {       
        var newwindow = "";
        try {
                url = "/dashboard/projectdirectorhousing/pdh_task_detail/"+id+"/?_popup=1"
                var  win = window.open(url,"Payment",'width=920,height=840,toolbar=0,menubar=0,location=0')
                var timer = setInterval(function() {   
                    if(win.closed) {  
                        clearInterval(timer);  
                        location.reload(); 
                    }  
                }, 1000);
            }
        catch(e)
            {
                alert(e);
            }
    };

    self.getUsers = function()
    {       

        try {

            var posturl             =   '/dashboard/projectdirectorhousing/get_users/';
            var retuntext           =   $.ajax({type: "POST", url: posturl, async: false}).responseText;

            retuntext = jQuery.parseJSON(retuntext);
            
            if(retuntext.status == 1)
            {
               return retuntext.data.users;
            }
            else
            {
                return retuntext.data.users;
            }
        }

        catch(e)
        {
            alert(e);
        }
    };

    self.getTaskActions = function(project_id,status_id)
    {       
        try {
            $.ajax({
                url: '/dashboard/projectdirectorhousing/get_task_actions/',
                type: "POST",
                data: {
                    project_id:project_id,
                    status_id:status_id,
                },
                success: function (res) {
                    $('#task_response').append(res)
                    $('html, body').animate({
                        scrollTop: $("#task_response").offset().top
                      }, 2000);
                  
                },
             
            });   // new script code
            return false;
        }

        catch(e)
        {
            alert(e);
        }
    };
    
    self.changeSeenStatus = function(task_action_id)
    {       
        try {
            $.ajax({
                url: '/dashboard/taskactionlist/change_seen_status/',
                type: "POST",
                data: {
                    task_action_id:task_action_id,
                },
                success: function (res) {
                    location.reload(false);
                },
            });   // new script code
            return false;
        }

        catch(e)
        {
            alert(e);
        }
    };
    
    
    self.getTaskActionsByTaskId = function(project_id,task_id)
    {       
        try {
            $.ajax({
                url: '/dashboard/projectdirectorhousing/get_task_actions_by_task_id/',
                type: "POST",
                data: {
                    project_id:project_id,
                    task_id:task_id,
                },
                success: function (res) {
                    $('#task_response').append(res)
                    $('html, body').animate({
                        scrollTop: $("#task_response").offset().top
                      }, 3000);
                  
                },
             
            });   // new script code
            return false;
        }

        catch(e)
        {
            alert(e);
        }
    };
    
  
    self.getNotificationTaskAction = function(comment_id)
    {       
        try {
            $.ajax({
                url: '/dashboard/projectdirectorhousing/get_notification_task_action/',
                type: "POST",
                data: {
                    comment_id:comment_id,
                },
                success: function (res) {
                    $('#task_response').append(res)
                    $('html, body').animate({
                        scrollTop: $("#task_response").offset().top
                      }, 2000);
                  
                },
             
            });   // new script code
            return false;
        }

        catch(e)
        {
            alert(e);
        }
    };

    self.getBellNotifications = function()
    {       
        try {
            $.ajax({
                url: '/dashboard/projectdirectorhousing/bell_notifications/',
                type: "POST",
                success: function (res) {
                    $('#navbar-notif-tab-2').append(res)
                },
            });   // new script code
            return false;
        }

        catch(e)
        {
            alert(e);
        }
    };
   
    self.getTaskActionAttachmentsJs = function(task_action_id)
    {       
        try {
            var response = $.ajax({
                url: '/dashboard/projectdirectorhousing/get_task_action_attachments/',
                type: "POST",
                data: {
                    task_action_id:task_action_id,
                },
                success: function (res) {
                    $('#modal_obsns_attachment #modal_obsns_attachment_body').append(res)
                },
                           
            });   // new script code
            
            return response;
        }

        catch(e)
        {
            alert(e);
        }
    };


    self.getInboxComments = function()
    {       

        try {

            var posturl             =   '/dashboard/projectdirectorhousing/get_inbox_comments/';
            var retuntext           =   $.ajax({type: "POST", url: posturl, async: false}).responseText;

            retuntext = jQuery.parseJSON(retuntext);
            
            if(retuntext.status == 1)
            {
               return retuntext.data.tagged_comments;
            }
            else
            {
                self.getPaymentVoucher();
            }
        }

        catch(e)
        {
            alert(e);
        }
    };

    self.obsnModal = function(obsn='')
    {       
        try{
            $("#task_action_obsn").text(obsn);
            $('#modalObsn').modal('toggle');    
        }
        catch(e)
        {
            alert(e);
        }
    };
    
    self.submitReply = function(){
        $(document).on('submit', '#reply_form', function(e) {

            var comment_id = $('#task_action_comment_id').val();
            var user_id = $('#reply_form #userList option:selected').val();
            var message = $("#message").val();
            if(comment_id != "" && user_id != "" && message != "")
            {
                alert(user_id)
            $.ajax({
                url: "/dashboard/pdh/comment_replay/",
                type: "GET",
                dataType: 'json', // added data type
                data: {
                    comment_id : comment_id,
                    template_id :  user_id,
                    comment : message,
                },
                success: function(res) {
                    location.reload(true);
                }
            });   // new script code
    
            }
        });
    }

    return self;
})();



// TO BE REMOVED
// ***************************************
// ***************************************
// ***************************************
// ***************************************
// ***************************************
// ***************************************


// self.OneLinkNdcTransactionWindow = function(id='')
//     {       var newwindow = "";
//         try {
//                 url = "/membership/ndc_onelink_payment/"+id+"/?_popup=1"
//                 var  win = window.open(url,"Payment",'width=920,height=840,toolbar=0,menubar=0,location=0')
//                 var timer = setInterval(function() {   
//                     if(win.closed) {  
//                         clearInterval(timer);  
//                         location.reload(); 
//                     }  
//                 }, 1000);
//             }
//         catch(e)
//             {
//                 alert(e);
//             }
//     };



//     self.IPGTransactionWindow = function(id='')
//     {       var newwindow = "";
//         try {
//                 url = "/membership/ndc_mastercard_payment/"+id+"/?_popup=1"
//                 var  win = window.open(url,"Payment",'width=920,height=840,toolbar=0,menubar=0,location=0')
//                 var timer = setInterval(function() {   
//                     if(win.closed) {  
//                         clearInterval(timer);  
//                         location.reload(); 
//                     }  
//                 }, 1000);
//             }
//         catch(e)
//             {
//                 alert(e);
//             }
//     };
    
    
//     self.IPGAllDuesTransactionWindow = function(id='')
//     {       var newwindow = "";
//         try {
//                 url = "/membership/ndc_alldues_mastercard_payment/"+id+"/?_popup=1"
//                 var  win = window.open(url,"Payment",'width=920,height=840,toolbar=0,menubar=0,location=0')
//                 var timer = setInterval(function() {   
//                     if(win.closed) {  
//                         clearInterval(timer);  
//                         location.reload(); 
//                     }  
//                 }, 1000);
//             }
//         catch(e)
//             {
//                 alert(e);
//             }
//     };


//     self.getPaymentVoucherModel = function(id='')
//     {       

//         try {
//                 localStorage.setItem("payment_schedule_detail_id", id);
//                 $("#account_head_title").html($("#account_head_title_"+id).html());
//                 $('#model_property_payment_voucher').modal('show'); 

//             }
//         catch(e)
//             {
//                 alert(e);
//             }
//     };

//     self.getPaidPaymentVoucherBox = function(id='')
//     {       

//         try {
//                 //property_payment_voucher_number 

//                 $("#main_payment_voucher_box").hide();

//                 var id =  localStorage.getItem("payment_schedule_detail_id"); 

//                 var posturl             =   '/membership/property_payment_voucher_number/'+id+'/';
//                 var retuntext           =   $.ajax({type: "GET", url: posturl, async: false}).responseText;

//                 retuntext = jQuery.parseJSON(retuntext);
                
//                 if(retuntext.status == 1)
//                 {
//                     localStorage.setItem("payment_challan_id", retuntext.data);
//                     $("#upload_payment_challan_id").val(retuntext.data);
//                     $("#upload_payment_voucher_box").show();

//                 }
//                 else
//                 {
//                     self.getPaymentVoucher();
//                 }

//             }
//         catch(e)
//             {
//                 alert(e);
//             }
//     };




//     self.getPaymentVoucher = function()
//     {       

//         try {
                
//                 $("#main_payment_voucher_box").hide();
//                 $("#generate_payment_voucher_box").show();

//                 var id =  localStorage.getItem("payment_schedule_detail_id"); 

//                 var posturl             =   '/membership/property_payment_voucher_info/'+id+'/';
//                 //var posturl             =   url;
//                 //var csrf_token          =   $('input[name="csrfmiddlewaretoken"]').val();
//                 //var postdata            =   "csrfmiddlewaretoken="+csrf_token+'&id='+id;
//                 var retuntext           =   $.ajax({type: "GET", url: posturl, async: false}).responseText;

//                 retuntext = jQuery.parseJSON(retuntext);
                
//                 if(retuntext.status == 1)
//                 {
//                     var payment_schedule_detail = retuntext.data.payment_schedule_detail;
//                     var payment_challan  = retuntext.data.payment_challan;

//                     $("#account_head_title").html(payment_schedule_detail.account_head_title);
//                     $("#due_date").val(payment_schedule_detail.due_date);
//                     $("#remaining_amount").val(payment_schedule_detail.remaining_amount);
//                     $("#payment_schedule_detail_id").val(payment_schedule_detail.id);

//                     // bank 
//                     var bank_select_html = "<option value=''> Please Select Bank</option>";

//                     $.each(retuntext.data.banks, function(key,obj) {
//                         bank_select_html = bank_select_html+ "<option value='"+obj.id+"'> "+obj.name+" "+obj.account_number+"</option>";
//                     }); 
//                     $("#bank").html(bank_select_html);

//                     if(payment_challan.bank)
//                         $('#bank').val(payment_challan.bank).trigger("change");

//                     // payment_method 
//                     var bank_select_html = "<option value=''> Please Select Type</option>";

//                     $.each(retuntext.data.payment_methods, function(key,obj) {
//                         bank_select_html = bank_select_html+ "<option value='"+obj.id+"'> "+obj.name+"</option>";
//                     }); 
//                     $("#payment_method").html(bank_select_html);

//                     if(payment_challan.payment_method)
//                         $('#payment_method').val(payment_challan.payment_method).trigger("change");



//                     // payment_method 
//                     var bank_select_html = "<option value=''  masking_format=''>Please Select National Identity Type</option>";

//                     $.each(retuntext.data.national_identity_types, function(key,obj) {
//                         bank_select_html = bank_select_html+ "<option value='"+obj.id+"' masking_format='"+obj.masking_format+"' > "+obj.name+" ("+obj.code+")</option>";
//                     }); 
//                     $("#national_identity_type").html(bank_select_html);

//                     if(payment_challan.payment_method)
//                         $('#national_identity_type').val(payment_challan.national_identity_type).trigger("change");

//                     //national_identity_number

//                     if(payment_challan.national_identity_number)
//                         $('#national_identity_number').val(payment_challan.national_identity_number);
//                         var masking_format = $("#national_identity_type").find('option:selected').attr("masking_format");
//                         $("#national_identity_number").inputmask(masking_format);

//                     if(payment_challan.cheque_number)
//                         $('#cheque_dd_no').val(payment_challan.cheque_number);

//                     if(payment_challan.cheque_date)
//                         $('#cheque_dd_date').val(payment_challan.cheque_date);
                    
//                     if(payment_challan.contact_number)
//                         $('#contact_no').val(payment_challan.contact_number);                    

//                     $("#payment_challan_id").val(payment_challan.id)

//                     localStorage.setItem("payment_challan_id", payment_challan.id);

//                   //$('#model_property_payment_voucher').modal('show');      

//                 }
//                 else
//                 {
//                     alert("Sorry! Some Error.");
//                 }

//             }
//         catch(e)
//             {
//                 alert(e);
//             }
//     };



//     self.submitPaymentVoucherinfo = function()
//     {       

//         try {
//                 $.ajax({
//                     url: $('#payment_voucher_form').attr("action"),
//                     type: $('#payment_voucher_form').attr("method"),
//                     dataType: "JSON",
//                     data: new FormData(document.querySelector("#payment_voucher_form")),
//                     processData: false,
//                     contentType: false,
//                     success: function (data, status)
//                     {
//                        if(data.status == 1)
//                        {
//                             $("#submit_challan_info_btn").hide();
//                             $("#download_challan_pdf_btn").show();
//                             $("#main_payment_voucher_box").show();
//                             $("#generate_payment_voucher_box").hide();
//                        }

//                     },
//                     error: function (xhr, desc, err)
//                     {
//                         alert(data.data);

//                     }
//                 });        
//             }
//         catch(e)
//             {
//                 alert(e);
//             }
//     };



//     self.getDownloadPaymentVoucher = function()
//     {       var newwindow = "";
//         try {
//                 var id =  localStorage.getItem("payment_challan_id"); 
                
//                 if(id != '')
//                 {

//                     url = "/membership/property_payment_voucher_download/"+id+"/?_popup=1"
//                     var  win = window.open(url,"Payment",'width=920,height=840,toolbar=0,menubar=0,location=0')
//                     var timer = setInterval(function() {   
//                         if(win.closed) {  
//                             clearInterval(timer);  
//                             location.reload(); 
//                         }  
//                     }, 1000);
//                 }
//             }
//         catch(e)
//             {
//                 alert(e);
//             }
//     };


//     self.UploadPaidPaymentChallan = function()
//     {
//         try {
//                 $("#UploadChallan_btn").attr('disabled','disabled');
//                 $("#UploadChallan_btn").html('<i class="fa fa-spinner fa-spin fa-1x fa-fw"></i>');
//                 var formElement = document.getElementById('paid_payment_challan_upload_form');
//                 if(true)
//                 {
//                 var posturl             =   $('#paid_payment_challan_upload_form').attr("action");
//                 $.ajax({
//                             url : posturl,
//                             type : "POST",
//                             data : new FormData(formElement),
//                             contentType : false,
//                             cache : false,
//                             processData : false,
//                             success : function(data) {
//                                 //var mydata      =   jQuery.parseJSON(data);
//                                 var mydata = data
//                                 $('#paid_payment_challan_upload_form')[0].reset();
//                           //  $("#postvideo").html('');
//                                 if(mydata.status==1)
//                                 {
//                                   alert(mydata.data);
//                                   location.reload();
//                                 }
//                                 else
//                                 {
//                                  alert(mydata.data);       
//                                 }
//                                  $("#UploadChallan_btn").html('Submit');
//                                 $("#UploadChallan_btn").removeAttr('disabled');

//                             },
//                             error : function() {
//                             }
//                     });
//                 }
//             }
//         catch(e)
//             {

//             }
//     };