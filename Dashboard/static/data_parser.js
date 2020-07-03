$(document).ready(function () {

    //web socket handling
    if ('WebSocket' in window) {
        connect('ws://localhost:1234/');
    }
    else {
        console.log("WebSockets don't seem to be supported on this browser.");
    }

    function connect(host) {
        ws = new WebSocket(host);
        ws.onopen = function () {
            console.log('Connected!');
        };

        ws.onmessage = function (evt) {
            var obj = JSON.parse(evt.data);

            if (obj.sectors[0].last_update != null) {

                document.getElementById("sector0_plants").innerHTML = obj.sectors[0].plants;
                document.getElementById("sector0_last_update").innerHTML = "Updated: " + obj.sectors[0].last_update + " ago";
                document.getElementById("sector0_errors").innerHTML = obj.sectors[0].errors;
                if (obj.sectors[0].watering == true) {
                    $('#sector0_water_btn').html('<span class="spinner-grow spinner-grow-sm mr-2" role="status"></span>Watering...');
                }
                else {
                    $('#sector0_water_btn').html('Standby');
                };
            };
            $('#sector0_water_btn').click(function () {
                console.log('Sector0 click');
            });

            if (obj.sectors[1].last_update != null) {

                document.getElementById("sector1_plants").innerHTML = obj.sectors[1].plants;
                document.getElementById("sector1_last_update").innerHTML = "Updated: " + obj.sectors[1].last_update + " ago";
                document.getElementById("sector1_errors").innerHTML = obj.sectors[1].errors;
                if (obj.sectors[1].watering == true) {
                    $('#sector1_water_btn').html('<span class="spinner-grow spinner-grow-sm mr-2" role="status"></span>Watering...');
                }
                else {
                    $('#sector1_water_btn').html('Standby');
                };
            };
            $('#sector1_water_btn').click(function () {
                console.log('Sector1 click');
            });

            if (obj.sectors[2].last_update != null) {

                document.getElementById("sector2_plants").innerHTML = obj.sectors[2].plants;
                document.getElementById("sector2_last_update").innerHTML = "Updated: " + obj.sectors[2].last_update + " ago";
                document.getElementById("sector2_errors").innerHTML = obj.sectors[2].errors;
                if (obj.sectors[2].watering == true) {
                    $('#sector2_water_btn').html('<span class="spinner-grow spinner-grow-sm mr-2" role="status"></span>Watering...');
                }
                else {
                    $('#sector2_water_btn').html('Standby');
                };
            };
            $('#sector2_water_btn').click(function () {
                console.log('Sector2 click');
            });

            if (obj.sectors[3].last_update != null) {

                document.getElementById("sector3_plants").innerHTML = obj.sectors[3].plants;
                document.getElementById("sector3_last_update").innerHTML = "Updated: " + obj.sectors[3].last_update + " ago";
                document.getElementById("sector3_errors").innerHTML = obj.sectors[3].errors;
                if (obj.sectors[3].watering == true) {
                    $('#sector3_water_btn').html('<span class="spinner-grow spinner-grow-sm mr-2" role="status"></span>Watering...');
                }
                else {
                    $('#sector3_water_btn').html('Standby');
                };
            };
            $('#sector3_water_btn').click(function () {
                console.log('Sector3 click');
            });

            if (obj.watertanks[0].last_update != null) {
                document.getElementById("watertank0_level_text").innerHTML = obj.watertanks[0].level + '<sup class="small">%</sup>';
                document.getElementById("watertank0_level_data_value").setAttribute("data-value", obj.watertanks[0].level);
                document.getElementById("watertank0_last_update").innerHTML = "Updated: " + obj.watertanks[0].last_update + " ago";
                document.getElementById("watertank0_errors").innerHTML = obj.watertanks[0].errors;
            };

            if (obj.plants[0].last_update != null) {
                document.getElementById("plant0_moisture_text").innerHTML = obj.plants[0].soil_moisture + '<sup class="small">%</sup>';
                document.getElementById("plant0_moisture").innerHTML = obj.plants[0].soil_moisture + '%';
                document.getElementById("plant0_moisture_data_value").setAttribute("data-value", obj.plants[0].soil_moisture);
                document.getElementById("plant0_last_update").innerHTML = "Updated: " + obj.plants[0].last_update + " ago";
                document.getElementById("plant0_name").innerHTML = obj.plants[0].name;
            };

            if (obj.plants[1].last_update != null) {
                document.getElementById("plant1_moisture_text").innerHTML = obj.plants[1].soil_moisture + '<sup class="small">%</sup>';
                document.getElementById("plant1_moisture").innerHTML = obj.plants[1].soil_moisture + '%';
                document.getElementById("plant1_moisture_data_value").setAttribute("data-value", obj.plants[1].soil_moisture);
                document.getElementById("plant1_last_update").innerHTML = "Updated: " + obj.plants[1].last_update + " ago";
                document.getElementById("plant1_name").innerHTML = obj.plants[1].name;
            };

            if (obj.plants[2].last_update != null) {
                document.getElementById("plant2_moisture_text").innerHTML = obj.plants[2].soil_moisture + '<sup class="small">%</sup>';
                document.getElementById("plant2_moisture").innerHTML = obj.plants[2].soil_moisture + '%';
                document.getElementById("plant2_moisture_data_value").setAttribute("data-value", obj.plants[2].soil_moisture);
                document.getElementById("plant2_last_update").innerHTML = "Updated: " + obj.plants[2].last_update + " ago";
                document.getElementById("plant2_name").innerHTML = obj.plants[2].name;
            };

            if (obj.plants[3].last_update != null) {
                document.getElementById("plant3_moisture_text").innerHTML = obj.plants[3].soil_moisture + '<sup class="small">%</sup>';
                document.getElementById("plant3_moisture").innerHTML = obj.plants[3].soil_moisture + '%';
                document.getElementById("plant3_moisture_data_value").setAttribute("data-value", obj.plants[3].soil_moisture);
                document.getElementById("plant3_last_update").innerHTML = "Updated: " + obj.plants[3].last_update + " ago";
                document.getElementById("plant3_name").innerHTML = obj.plants[3].name;
            };

            if (obj.plants[4].last_update != null) {
                document.getElementById("plant4_moisture_text").innerHTML = obj.plants[4].soil_moisture + '<sup class="small">%</sup>';
                document.getElementById("plant4_moisture").innerHTML = obj.plants[4].soil_moisture + '%';
                document.getElementById("plant4_moisture_data_value").setAttribute("data-value", obj.plants[4].soil_moisture);
                document.getElementById("plant4_last_update").innerHTML = "Updated: " + obj.plants[4].last_update + " ago";
                document.getElementById("plant4_name").innerHTML = obj.plants[4].name;
            };

            if (obj.plants[5].last_update != null) {
                document.getElementById("plant5_moisture_text").innerHTML = obj.plants[5].soil_moisture + '<sup class="small">%</sup>';
                document.getElementById("plant5_moisture").innerHTML = obj.plants[5].soil_moisture + '%';
                document.getElementById("plant5_moisture_data_value").setAttribute("data-value", obj.plants[5].soil_moisture);
                document.getElementById("plant5_last_update").innerHTML = "Updated: " + obj.plants[5].last_update + " ago";
                document.getElementById("plant5_name").innerHTML = obj.plants[5].name;
            };

            if (obj.plants[6].last_update != null) {
                document.getElementById("plant6_moisture_text").innerHTML = obj.plants[6].soil_moisture + '<sup class="small">%</sup>';
                document.getElementById("plant6_moisture").innerHTML = obj.plants[6].soil_moisture + '%';
                document.getElementById("plant6_moisture_data_value").setAttribute("data-value", obj.plants[6].soil_moisture);
                document.getElementById("plant6_last_update").innerHTML = "Updated: " + obj.plants[6].last_update + " ago";
                document.getElementById("plant6_name").innerHTML = obj.plants[6].name;
            };

            if (obj.plants[7].last_update != null) {
                document.getElementById("plant7_moisture_text").innerHTML = obj.plants[7].soil_moisture + '<sup class="small">%</sup>';
                document.getElementById("plant7_moisture").innerHTML = obj.plants[7].soil_moisture + '%';
                document.getElementById("plant7_moisture_data_value").setAttribute("data-value", obj.plants[7].soil_moisture);
                document.getElementById("plant7_last_update").innerHTML = "Updated: " + obj.plants[7].last_update + " ago";
                document.getElementById("plant7_name").innerHTML = obj.plants[7].name;
            };

            if (obj.power[0].last_update != null) {
                var pwr = obj.power[0].level;
                document.getElementById('battery0_pwr_level').innerText = pwr + '%';
                document.getElementById("battery0_pwr_level_show").setAttribute("style", "width:calc(" + pwr + "% * 0.73)");
                document.getElementById("battery0_last_update").innerHTML = "Updated: " + obj.power[0].last_update + " ago";
                document.getElementById("battery0_state").innerHTML = obj.power[0].state;
                document.getElementById("battery0_errors").innerHTML = obj.power[0].errors;
            }

            for (var prop in obj.notifications) {
                document.getElementById('home').innerHTML += ('<div class="alert alert-' + obj.notifications[prop].type + ' alert-dismissible fade show" role="alert">' +
                    '<strong>' + obj.notifications[prop].timestamp + ' </strong>' + obj.notifications[prop].text +
                    '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                    '<span aria-hidden="true" >&times;</span>' +
                    '</button></div>');
            }

            $(".progress").each(function () {
                var value = $(this).attr('data-value');
                var left = $(this).find('.progress-left .progress-bar');
                var right = $(this).find('.progress-right .progress-bar');

                if (value > 0) {
                    if (value <= 50) {
                        right.css('transform', 'rotate(' + percentageToDegrees(value) + 'deg)')
                    } else {
                        right.css('transform', 'rotate(180deg)')
                        left.css('transform', 'rotate(' + percentageToDegrees(value - 50) + 'deg)')
                    }
                }

            })

            function percentageToDegrees(percentage) {
                return percentage / 100 * 360
            }

        };

        ws.onclose = function () {
            console.log('Socket connection was closed!!!');
        };

        setInterval(function () { ws.send("Hello server"); }, 2000);

    };
});