const fetch_data = async () => {
    let shop_id = $("#shop_id").val();
    if (!shop_id) {
        alert("ショップコードを入力してください。");
        return;
    }
    else {
        await eel.fetch_data(shop_id=shop_id);
    }
}

eel.expose(output_oder_list)
function output_oder_list(text) {
    let output_text = $("#output-data").val() + text + "\n";
    $("#output-data").val(output_text);
    $("#output-data").scrollTop($("#output-data")[0].scrollHeight);
}

// eel.expose(reset_object)
// function reset_object() {
//     document.order_form.reset();
// }


eel.expose(alert_js)
function alert_js(text) {
    alert(text);
}