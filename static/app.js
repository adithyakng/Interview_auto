// Setup the calendar with the current date
$(document).ready(function(){
    var date = new Date();
    console.log(date.getDate()+" aaa");
    var today = date.getDate();
    // Set click handlers for DOM elements
    $(".right-button").click({date: date}, next_year);
    $(".left-button").click({date: date}, prev_year);
    $(".month").click({date: date}, month_click);
    // $("#add-button").click({date: date}, new_event);
    // // Set current month as active
    // $(".months-row").children().eq(date.getMonth()).addClass("active-month");
    init_calendar(date);
   // var check=func(today,date.getMonth()+1,date.getFullYear());
    //var events = check_events(today, date.getMonth()+1, date.getFullYear());
    //show_events(events, months[date.getMonth()], today);
});


function func(day,month,year){
    
    var slot_date={
        'day':day.toString(),
        'month':month.toString(),
        'year':year.toString()
    };
    //console.log('adithya');
    console.log(slot_date);
    var xhttp=new XMLHttpRequest();
    xhttp.onreadystatechange=function(){
        if(this.status==200 && this.readyState==4)
        {
            var reply=JSON.parse(this.responseText);
            reply=reply['reply'];
            show_events(reply,month,day,year);
        }
    };
    xhttp.open("POST","/getSlots",true);
    xhttp.setRequestHeader('Content-Type','application/json');
    xhttp.send(JSON.stringify(slot_date));
}

// Initialize the calendar by appending the HTML dates
function init_calendar(date) {
    $(".tbody").empty();
    $(".events-container").empty();
    var calendar_days = $(".tbody");
    var month = date.getMonth();
    var year = date.getFullYear();
    var day_count = days_in_month(month, year);
    var row = $("<tr class='table-row'></tr>");
    var today = date.getDate();
    // Set date to 1 to find the first day of the month
    date.setDate(1);
    var first_day = date.getDay();
    //console.log(date.getDay());
    // 35+firstDay is the number of date elements to be added to the dates table
    // 35 is from (7 days in a week) * (up to 5 rows of dates in a month)
    for(var i=0; i<35+first_day; i++) {
        // Since some of the elements will be blank, 
        // need to calculate actual date from index
        var day = i-first_day+1;
        // If it is a sunday, make a new row
        if(i%7===0) {
            calendar_days.append(row);
            row = $("<tr class='table-row'></tr>");
        }
        // if current index isn't a day in this month, make it blank
        if(i < first_day || day > day_count) {
            var curr_date = $("<td class='table-date nil'>"+"</td>");
            row.append(curr_date);
        }   
        else {
            var curr_date = $("<td class='table-date'>"+day+"</td>");
            var events=[];
           // var events = check_events(day, month+1, year);
            if(today===day && $(".active-date").length===0) {
                curr_date.addClass("active-date");
               // show_events(events, months[month], day);       
            }
            // If this date has any events, style it with .event-date
            if(events.length!==0) {
                curr_date.addClass("event-date");
            }
            // Set onClick handler for clicking a date
            curr_date.click({year:year,month: month, day:day}, date_click);
            row.append(curr_date);
        }
    }
    // Append the last row and set the current year
    calendar_days.append(row);
    $(".year").text(year);
}

// Get the number of days in a given month/year
function days_in_month(month, year) {
    var monthStart = new Date(year, month, 1);
    var monthEnd = new Date(year, month + 1, 1);
    return (monthEnd - monthStart) / (1000 * 60 * 60 * 24);    
}

// Event handler for when a date is clicked
function date_click(event) {
    $(".events-container").show(250);
    $("#dialog").hide(250);
    $(".active-date").removeClass("active-date");
    $(this).addClass("active-date");
    func(event.data['day'],event.data['month']+1,event.data['year'])
    //show_events(event.data.events, event.data.month, event.data.day);
};



// Display all events of the selected date in card views
function show_events(events, month, day,year) {
    // Clear the dates container
   //console.log(events);

    $(".events-container").empty();
    $(".events-container").show(250);
    //console.log(event_data["events"]);
    // If there are no events for this date, notify the user
    if(events.length===0) {
        var event_card = $("<div class='event-card'></div>");
        var event_name = $("<div class='event-name'>All slots are full for "+day+".</div>");
        $(event_card).css({ "border-left": "10px solid #FF1744" });
        $(event_card).append(event_name);
        $(".events-container").append(event_card);
    }
    else {
        // Go through and add each event as a card to the events container
        var combinedslots=getCombinedSlots(events).sort();
        console.log(combinedslots+" adithya");
        for(var i=0; i<combinedslots.length; i++) {
            var event_card = $("<div class='event-card'></div>");
            var event_name = $("<div class='event-name'><input type='radio' name='slot' value='"+combinedslots[i]+"'>"+combinedslots[i]+"</div>");
          
            
            $(event_card).append(event_name)
            $(".events-container").append(event_card);
        }
        var select_slot=$("<div class='select-slot'><button type='button' class='select' id='select'>"+"SELECT"+"</button></div>");
        $(".events-container").append(select_slot);
        $(".select").click({day: day,month:month,year:year}, slot_push);

    }
}
var selected_slots=[]
var max_slots=3;
var selected_dates=[]
function slot_push(slot_date)
{
    if(selected_slots.length==max_slots)
    {
        $(".sub_button").show();
    }
    if(selected_slots.length<max_slots){
    slot_date=slot_date.data;
    console.log(slot_date);
    var flag=0;
    //var ele = document.getElementById('select');
    extract_slot=$('input[name="slot"]:checked').val();
    var push={
        'day':slot_date['day'],
        'month':slot_date['month'],
        'year':slot_date['year'],
        'slot':extract_slot
    };
    if(already_pushed(push))
    {
        $('#present').html("Slot already selected");
    }
    else
    {
        display_function(push);
        selected_slots.push(push);
        console.log(selected_slots);
        $('#present').html("");
        if(selected_slots.length==max_slots)
        {
            $(".sub_button").show();
        }
        $('.clear').show();
    }
}
else
{
    $('#max').html("Max slots reached");
    console.log("Max slots reached");
}

}
function clear_slots()
{
    for(var i=0;i<max_slots;i++)
    {
        var slot_number='#'+'slot'+i.toString();
        $(slot_number).html("");
        selected_slots=[];
    }
    $('.clear').hide();
}
function already_pushed(push)
{
    for (var i=0;i<selected_slots.length;i++)
    {
        if(push['day']==selected_slots[i]['day'] && push['month']==selected_slots[i]['month']&&
        push['year']==selected_slots[i]['year'] && push['slot']==selected_slots[i]['slot'] )
        {
            return true;
        }
    }
    return false;
}

function final_subm()
{
    console.log('adithya');
    var xhttp=new XMLHttpRequest();
    xhttp.onreadystatechange=function(){
        if(this.readyState==4 && this.status==200)
        {
            console.log(this.responseText);
            var reply=JSON.parse(this.responseText);
            if(reply['reply']=='fail'){
                window.location.href='/slot_fail'
            }
            else{
            window.location.href='/slot_details';
            }
        }
    };
    xhttp.open('POST','/assign_slot',true);
    xhttp.setRequestHeader('Content-Type','application/json');
    xhttp.send(JSON.stringify(selected_slots));
}

function display_function(push)
{
    var slot_number='#'+'slot'+selected_slots.length.toString();
    console.log(slot_number);
    $(slot_number).html('Your slot is booked on '+push['day']+"/"+push['month']+"/"+push['year']+" at "+push['slot']);
}


//Get Combined Slots

function getCombinedSlots(events)
{
    var timeslots=[];
    for (var i=0;i<events.length;i++)
    {
        var slots=events[i]['slots'];
        for(var j=0;j<slots.length;j++)
        {
            if(!timeslots.includes(slots[j]))
                timeslots.push(slots[j]);
        }
    }
    return timeslots;
}


// Event handler for when a month is clicked
function month_click(event) {
    $(".events-container").show(250);
    $("#dialog").hide(250);
    var date = event.data.date;
    $(".active-month").removeClass("active-month");
    $(this).addClass("active-month");
    var new_month = $(".month").index(this);
    date.setMonth(new_month);
    init_calendar(date);
}

// Event handler for when the year right-button is clicked
function next_year(event) {
    $("#dialog").hide(250);
    var date = event.data.date;
    var new_year = date.getFullYear()+1;
    $("year").html(new_year);
    date.setFullYear(new_year);
    init_calendar(date);
}

// Event handler for when the year left-button is clicked
function prev_year(event) {
    $("#dialog").hide(250);
    var date = event.data.date;
    var new_year = date.getFullYear()-1;
    $("year").html(new_year);
    date.setFullYear(new_year);
    init_calendar(date);
}

