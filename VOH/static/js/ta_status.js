function get_ta_status(data) {
    if (data){
        var html_data = "";
        mydiv = Document.getElementById('ta_status');
        for (var i = 0; i< Object.keys(data).length; i++) {
            var ta_name = data[i]["net_id"];
            var ta_status = data[i]["status"];
            html_data.append("<div><span>ta_name:ta_status</span></div>");
        }
        mydiv.html("");
        mydiv.html(html_data);
    }

}
/**
 * Created by Aadhya on 4/14/16.
 */
$.ajax({
    url: "/update_ta_status/",
    method: "post",
    success:function(data){
        get_ta_status(data);
    }
});