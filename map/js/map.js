var gdata = {io:{handleScriptLoaded:function(data){callback(data)}}},
    talks = {
        sat: {
            '9'  : {'B':' ','C':' ','D':' ','E':' ','F':' ','G':' ','H':' ','I':' ','J':' '}, //event-wide (regi/breakfast)
            '10' : {'B':' ','C':' ','D':' ','E':' ','F':' ','G':' ','H':' ','I':' ','J':' '}, //event-wide (plenary/intro)
            '12' : {'B':' ','C':' ','D':' ','E':' ','F':' ','G':' ','H':' ','I':' ','J':' '},
            '13' : {'B':' ','C':' ','D':' ','E':' ','F':' ','G':' ','H':' ','I':' ','J':' '},
            '14' : {'B':' ','C':' ','D':' ','E':' ','F':' ','G':' ','H':' ','I':' ','J':' '},
            '15' : {'B':' ','C':' ','D':' ','E':' ','F':' ','G':' ','H':' ','I':' ','J':' '}, //event-wide (lunch)
            '16' : {'B':' ','C':' ','D':' ','E':' ','F':' ','G':' ','H':' ','I':' ','J':' '},
            '17' : {'B':' ','C':' ','D':' ','E':' ','F':' ','G':' ','H':' ','I':' ','J':' '},
            '18' : {'B':' ','C':' ','D':' ','E':' ','F':' ','G':' ','H':' ','I':' ','J':' '},
            '19' : {'B':' ','C':' ','D':' ','E':' ','F':' ','G':' ','H':' ','I':' ','J':' '},
            '20' : {'B':' ','C':' ','D':' ','E':' ','F':' ','G':' ','H':' ','I':' ','J':' '},
            '21' : {'B':' ','C':' ','D':' ','E':' ','F':' ','G':' ','H':' ','I':' ','J':' '},
            '22' : {'B':' ','C':' ','D':' ','E':' ','F':' ','G':' ','H':' ','I':' ','J':' '}, //event-wide (afterparty)
            '23' : {'B':' ','C':' ','D':' ','E':' ','F':' ','G':' ','H':' ','I':' ','J':' '} //event-wide (end of day 1)
        },
        sun : {
            '9'  : {'B':' ','C':' ','D':' ','E':' ','F':' ','G':' ','H':' ','I':' ','J':' '}, //event-wide (regi/breakfast)
            '10' : {'B':' ','C':' ','D':' ','E':' ','F':' ','G':' ','H':' ','I':' ','J':' '},
            '11' : {'B':' ','C':' ','D':' ','E':' ','F':' ','G':' ','H':' ','I':' ','J':' '},
            '12' : {'B':' ','C':' ','D':' ','E':' ','F':' ','G':' ','H':' ','I':' ','J':' '},
            '13' : {'B':' ','C':' ','D':' ','E':' ','F':' ','G':' ','H':' ','I':' ','J':' '},
            '14' : {'B':' ','C':' ','D':' ','E':' ','F':' ','G':' ','H':' ','I':' ','J':' '},
            '15' : {'B':' ','C':' ','D':' ','E':' ','F':' ','G':' ','H':' ','I':' ','J':' '}, //event-wide (lunch)
            '16' : {'B':' ','C':' ','D':' ','E':' ','F':' ','G':' ','H':' ','I':' ','J':' '},
            '17' : {'B':' ','C':' ','D':' ','E':' ','F':' ','G':' ','H':' ','I':' ','J':' '},
            '18' : {'B':' ','C':' ','D':' ','E':' ','F':' ','G':' ','H':' ','I':' ','J':' '},
            '19' : {'B':' ','C':' ','D':' ','E':' ','F':' ','G':' ','H':' ','I':' ','J':' '}, //event-wide (Closing Session)
            '20' : {'B':' ','C':' ','D':' ','E':' ','F':' ','G':' ','H':' ','I':' ','J':' '} //event-wide (Doors close)
        }
    },
    isSat = true,
    rooms = {
        'B': 'horace-mann',
        'C': 'thomas-paul',
        'D': 'deborah-sampson',
        'E': 'abigail-adams',
        'F': 'crispus-attacks',
        'G': 'area-1220',
        'H': 'area-1235',
        'I': 'area-1255',
        'J': '11th-floor'
    };


function callback(data) {
    function processCell(talk) {
        var c = splitCellName(talk.title.$t);
        if (c) {
            talks[(isSat ? 'sat' : 'sun')][c[1]][c[0]] = talk.content.$t
        }
    }
    
    function splitCellName(title) {
        var col = title[0],
            row = title.substring(1)
        if ((rooms[col]) && (talks[(isSat ? 'sat' : 'sun')][row])) {
            return [col, row]
        } else {
            return false
        }
    }

    var cells = data.feed.entry;

    for (var x=0, len=cells.length; x < len; x++) {
        processCell(cells[x])
    }
    // If saturday, load sunday
    if (isSat) {
        $("head").append('<script src="https://spreadsheets.google.com/feeds/cells/0AiPSd498xaohdGMzdzJNcnF5eE9zV3Q1UFp6T0t5c1E/od5/public/basic?alt=json-in-script"><\/script>')
        isSat = false
    }
}

Raphael.fn.arrow = function(x1, y1, x2, y2, size) {
    var angle = Raphael.angle(x1, y1, x2, y2),
        a45   = Raphael.rad(angle-45),
        a45m  = Raphael.rad(angle+45),
        a135  = Raphael.rad(angle-135),
        a135m = Raphael.rad(angle+135),
        x1a = x1 + Math.cos(a135) * size,
        y1a = y1 + Math.sin(a135) * size,
        x1b = x1 + Math.cos(a135m) * size,
        y1b = y1 + Math.sin(a135m) * size,
        x2a = x2 + Math.cos(a45) * size,
        y2a = y2 + Math.sin(a45) * size,
        x2b = x2 + Math.cos(a45m) * size,
        y2b = y2 + Math.sin(a45m) * size;
    return this.path(
        "M"+x2+" "+y2+"L"+x1+" "+y1+
        "M"+x1+" "+y1+"L"+x1a+" "+y1a+"L"+x1b+" "+y1b+"L"+x1+" "+y1+"Z"
    ).attr({'fill':'black'});
};

function selectTime(cur) {
    // sat:
    // 0=9, 1=10, 2=11, 3=11:40, 4=12:20, 5=1, 6=2, 7=2:40, 8=3:20, 9=4, 10=4:40, 11=5:20, 12=6, 13=9
    // sun:
    // 14=9, 15=10, 16=10:40, 17=11:20, 18=12, 19=12:30, 20=1, 21=2, 22=2:40, 23=3:20, 24=4, 25=5
    var x = 0,
        sat = 6,
        sun = 7,
        month = 3,
        year = 2012;
    if ((cur.getFullYear() == year)&&(cur.getMonth() == month)) {
        var d = cur.getDay(), // 0-30(31, leap)
            h = cur.getHours(), // 0-23
            m = cur.getMinutes(); // 0-59
        if (d < sat) {
            x = 0;
        } else if (d == sat) { 
            if (h <= 9) {
                x = 0;
            } else if (h == 10) {
                x = 1;
            } else if ((h == 11)&&(m<40)) {
                x = 2;
            } else if ((h <= 12)&&(m<20)) {
                x = 3;
            } else if (h < 13) {
                x = 4;
            } else if (h < 14) {
                x = 5;
            } else if ((h == 14)&&(m<40)) {
                x = 6;
            } else if ((h <= 15)&&(m<20)) {
                x = 7;
            } else if (h < 16) {
                x = 8;
            } else if ((h == 16)&&(m<40)) {
                x = 9;
            } else if ((h <= 17)&&(m<20)) {
                x = 10;
            } else if (h < 18) {
                x = 11;
            } else if (h < 21) {
                x = 12;
            } else {
                x = 13;
            }
        } else if (d == sun) {
            if (h <= 9) {
                x = 14;
            } else if ((h == 10)&&(m < 40)) {
                x = 15;
            } else if ((h <= 11)&&(m < 20)) {
                x = 16;
            } else if (h < 12) {
                x = 17;
            } else if ((h == 12)&&(m < 30)) {
                x = 18;
            } else if (h < 13) {
                x = 19;
            } else if (h < 14) {
                x = 20;
            } else if ((h == 14)&&(m < 40)) {
                x = 21;
            } else if ((h <= 15)&&(m < 20)) {
                x = 22;
            } else if (h < 16) {
                x = 23;
            } else if (h < 17) {
                x = 24;
            } else {
                x = 25;
            }
        } else {
            x = 25;
        }
    } else {
        x = 25;
    }
    $("#nav-select").prop("selectedIndex", x)
}

$(function() {
    var tip = $("#tip").hide(),
        tipText = "",
        over = false;

    function addTalksToTooltip(dayNum) {
        var day = dayNum.substring(0,3),
            num = dayNum.substring(3);
        for (var talk in talks[day][num]) {
            (function() {
                var room = '#'+rooms[talk];
                var text = talks[day][num][talk]
                $(room+' p').html(text)
            })()
        }
        makeTooltips();
    }
            
    function makeTooltips() {
        var current = null;
        for (var state in map) {
            map[state].color = Raphael.getColor();
            (function (st, state) {
                st[0].style.cursor = "pointer";
                var stateID = '#'+state;
                var stateContent = $(stateID).html();
                $(st[0]).mouseover(function(){
                    map[state].animate({fill: "#666", stroke: "#000"}, 500) ;
                    document.getElementById(state).style.display = "";
                    st.animate({fill: st.color, stroke: "#000"}, 500);
                    st.toFront();
                    R.safari();
                    tipText = stateContent;
                    $(tip).stop(true, true).fadeIn();
                    over = true;
                }).mouseout(function(){
                    st.animate({fill: "#666", stroke: "#000"}, 500);
                    st.toFront();
                    R.safari();
                    $(tip).stop(true, true).fadeOut();
                    over = false;
                });
            })(map[state], state);
        }
        $("#paper").mousemove(function(e){
            e = e || window.event;
            if (over){
                o = $(this).offset();
                $(tip).css("left", (e.pageX-o.left)-100).css("top", (e.pageY-o.top)+20);
                $(tip).html(tipText);
            }
        });
    }

    var R = Raphael("paper", 750, 440),
        attr_bg = {
            fill: "#999",
            stroke: "#000",
            "stroke-width": 1,
            "stroke-linejoin": "round"
        },
        attr_empty = {
            fill: "#1e1e1e",
            stroke: "#000",
            "stroke-width": 1,
            "stroke-linejoin": "round"
        },
        attr = {
            fill: "#666",
            stroke: "#000",
            "stroke-width": 1,
            "stroke-linejoin": "round"
        },
        map_background = {
            'background'      : R.path("M 120.8 60.1 L 345.2 60.1 L 345.2 25.3 L 488.9 25.3 L 488.9 75.1 L 578.4 75.1 L 578.4 25.3 L 723.3 25.3 L 723.3 75.1 L 723.3 141 L 505.1 141 L 358.3 414.6 L 30.6 267.4Z").attr(attr_bg),
            'empty_zone'      : R.path("M 377 307.6 L 465.9 141.6 L 358.3 141.6 L 358.3 307.6Z").attr(attr_empty),
        },
        map = {
            'deborah-sampson' : R.path("M 247.6 213.1 L 156.2 213.1 L 156.2 254.8 L 247.6 307.6Z").attr(attr),
            'horace-mann'     : R.path("M 247.6 141.6 L 358.3 141.6 L 358.3 307.6 L 247.6 307.6Z").attr(attr),
            'thomas-paul'     : R.path("M 247.6 141.6 L 156.2 141.6 L 156.2 213.7 L 247.6 213.7Z").attr(attr),
            'abigail-adams'   : R.path("M 578.4 25.3 L 578.4 75.1 L 650.9 75.1 L 650.9 25.3Z").attr(attr),
            'crispus-attacks' : R.path("M 650.3 25.3 L 650.3 75.1 L 723.3 75.1 L 723.3 25.3Z").attr(attr),
            'area-1220'       : R.path("M 156.2 60.1 L 156.2 100.1 L 345.2 100.1 L 345.2 60.1Z").attr(attr),
            'area-1235'       : R.path("M 94 218.8 L 110.7 179.5 L 156.2 179.5 L 156.2 254.8Z").attr(attr),
            'area-1255'       : R.path("M 307.3 307.6 L 307.3 347.4 L 350.2 359.9 L 377 307.6Z").attr(attr),
            '11th-floor'      : R.circle(600, 285, 100).attr(attr)
        },
        map_text = {
            'cafe'            : R.text(418, 47, 'Cafe Area').attr({'font-size': 16}),
            'up'     : R.arrow(433, 220, 433, 240, 7),
            'down'     : R.arrow(443, 240, 443, 220, 7),
            'paul-door'     : R.arrow(150, 165, 135, 165, 7),
            'sampson-door'     : R.arrow(190, 282, 190, 297, 7),
            'mann-door'     : R.arrow(345, 135, 345, 120, 7),
            'paul-door'     : R.arrow(150, 165, 135, 165, 7),
            'adams-door'     : R.arrow(595, 82, 595, 97, 7),
            'attacks-door'     : R.arrow(692, 82, 692, 97, 7),
            '1235-door'     : R.arrow(100, 187, 85, 187, 7),
            '1235-door-2'   : R.arrow(133, 249, 133, 264, 7),
            '1255-door'     : R.arrow(301, 326, 286, 326, 7),
            '1255-door-2'   : R.arrow(373, 326, 388, 326, 7)
        };

    $('#nav-select').change(function() { 
        addTalksToTooltip(this.value) 
    })

    selectTime(new Date());

    addTalksToTooltip($('#nav-select').val());

})



