function returnTagCount() {
    var i = 1;
    var count = 0;
    currentElement = document.getElementById(i);
    while (currentElement){
        if (!currentElement.classList.contains('tag-unclicked')) {
            count = count + 1;
        }
        i += 1; currentElement = document.getElementById(i);
    }
    return count;
}

function getFilteredTagNames() {
    var i = 1;
    currentElement = document.getElementById(i);
    var out = [];
    while (currentElement){
        if (!currentElement.classList.contains('tag-unclicked')) {
            var name = currentElement.classList[4];
            out.push(name);
        }
        i += 1;
        currentElement = document.getElementById(i);
    }
    return out;
}


function makeDefaultImage(source) {
    var myColors = ["06acc2", "08c262", "6e73ff", "7bff00", "ff006f"];
    var randomInt = Math.round(Math.random()*(myColors.length));
    var randomColor = myColors[randomInt];
    var URL = "https://dummyimage.com/600x400/"+randomColor+"/0011ff&text=+"
    source.src = URL;
    source.onerror=null;
    console.log(source);
}
function makeAllInvisible() {
    var allProjects = document.getElementsByClassName('project');
    for (var i = 0; i < allProjects.length; i++) {
        allProjects[i].classList.add('d-none');
    }
}

function makeAllVisible() {
    var allProjects = document.getElementsByClassName('project');
    for (var i = 0; i < allProjects.length; i++) {
        allProjects[i].classList.remove('d-none');
    }
}

function badgeClicked(num) {
    document.getElementById(num).childNodes[1].classList.toggle('cross-clicked');
    var tagName = document.getElementById(num).classList[4];
    // user selected tag
    if (document.getElementById(num).classList.contains('tag-unclicked')) {
        document.getElementById(num).classList.toggle('tag-unclicked');
        document.getElementById(num).style.backgroundColor = document.getElementById(num).classList[3];
        var numSelected = returnTagCount();
        // if the first tag is selected, make all invisible and grab tagged items
        if (numSelected == 1) {
            makeAllInvisible();
            console.log(tagName);
            var taggedProjects = document.getElementsByClassName('project '+tagName);
            console.log(taggedProjects);
            for (var i = 0; i < taggedProjects.length; i++) {
                taggedProjects[i].classList.remove('d-none');
            }
        }
        else {
            var tags = getFilteredTagNames();
            var classString = "";
            for (var i = 0; i < tags.length; i++) {
                classString += tags[i] + " ";
            }
            makeAllInvisible();
            var toFilter = document.getElementsByClassName(classString);
            for (var i = 0; i < toFilter.length; i++) {
                toFilter[i].classList.remove('d-none');
            }
        }
    }
    // user unselected tag
    else {
        document.getElementById(num).style.backgroundColor = '#a0a0a0';
        document.getElementById(num).classList.toggle('tag-unclicked');
        var numSelected = returnTagCount();
        if (numSelected == 0) {
            makeAllVisible();
        }
        else {
            var tags = getFilteredTagNames();
            var classString = "";
            for (var i = 0; i < tags.length; i++) {
                classString += tags[i] + " ";
            }
            makeAllInvisible();
            var toFilter = document.getElementsByClassName(classString);
            for (var i = 0; i < toFilter.length; i++) {
                toFilter[i].classList.remove('d-none');
            }

        }
    }

}

/*document.getElementById("num_developers").onchange = function()
{
    var numDevelopers = parseInt(this.value);
    $(".dev-option").remove();
    for (var i = 0; i < numDevelopers; i++) {
        var form = document.getElementById('developers');
        var innerHTML = '<input class="form-control dev-option" id="developers" name="developers" placeholder="Developer #' + parseInt(i+1)+'" type="text" /> <br>'
        form.innerHTML += innerHTML;
    }
};
*/

$(function() {
    $('#btn_submit').click(function() {
        var form_data = new FormData($('form')[0]);
        var tags = getFilteredTagNames();
        form_data.append("tags", tags);
        $.ajax({
            url: '/submit',
            type: 'POST',
            data: form_data,
            processData: false,
            contentType: false,
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});

$(function() {
    $('#add_tag_btn_submit').click(function() {
        var form_data = new FormData($('form')[0]);
        $.ajax({
            url: '/admin/tags',
            type: 'POST',
            data: form_data,
            processData: false,
            contentType: false,
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});

function parseDevNames(names, githubs) {
    var nameList = names.split(',');
    var githubList = githubs.split(',');
    var numCols = 12/(nameList.length);
    var imageRow = document.getElementById('image-row');
    for (var i = 0; i < nameList.length; i++) {
        var imageUrl = "https://github.com/"+githubList[i]+".png";
        var githubUrl = "https://github.com/"+githubList[i];
        var githubName = "@"+githubList[i];
        var toAdd = "<div class='col-md-" + numCols.toString() + "'><div class='text-center'><img src='"+imageUrl+"' onerror='makeDefaultImage(this)' class='round-img' width='200px' height='200px'/><br><br>"+nameList[i]+"<br><small><a href='"+githubUrl+"' class='github-user' target='_blank'>"+githubName+"</a></small></div></div>";

        imageRow.innerHTML += toAdd;
    }
}

function approveRows(rowNumber) {
    var tr = document.getElementById('adminTable')
        .getElementsByTagName('tr')[rowNumber];
    tr.classList.remove('table-danger');
    tr.classList.toggle('table-success');

    document.getElementById(rowNumber).style.display='none';

}

function rejectRows(rowNumber) {
    var tr = document.getElementById('adminTable')
        .getElementsByTagName('tr')[rowNumber];
    tr.classList.remove('table-success');
    tr.classList.toggle('table-danger');
    var buttonStyle = document.getElementById(rowNumber).style.display;
    if (buttonStyle === "none") {
        document.getElementById(rowNumber).style.display = 'inline-block';
    }
    else {
        document.getElementById(rowNumber).style.display = 'none';
    }
}

function featureRows(rowNumber) {
    var tr = document.getElementById('adminTable')
        .getElementsByTagName('tr')[rowNumber];
    tr.classList.toggle('table-secondary');
}

function checkboxAction() {
    var pending = document.getElementById('pending-checkbox').checked;
    var approved = document.getElementById('approved-checkbox').checked;
    var submitted = document.getElementById('feedback-checkbox').checked;
    var featured = document.getElementById('featured-checkbox').checked;
    if (pending) {
        var pendingItems = document.getElementsByClassName('pending');
        var i;
        for (i=0; i < pendingItems.length; i++) {
            pendingItems[i].style.display = null;
        }
    }
    else if (!pending) {
        var pendingItems = document.getElementsByClassName('pending');
        var i;
        for (i=0; i < pendingItems.length; i++) {
            pendingItems[i].style.display = 'none';
        }
    }
    if (approved) {
        var approvedItems = document.getElementsByClassName('approved');
        var i;
        for (i=0; i < approvedItems.length; i++) {
            approvedItems[i].style.display = null;
        }
    }
    else if (!approved) {
        var approvedItems = document.getElementsByClassName('approved');
        var i;
        for (i=0; i < approvedItems.length; i++) {
            approvedItems[i].style.display = 'none';
        }
    }
    if (submitted) {
        var submittedItems = document.getElementsByClassName('submitted');
        var i;
        for (i=0; i < submittedItems.length; i++) {
            submittedItems[i].style.display = null;
        }
    }
    else if (!submitted) {
        var submittedItems = document.getElementsByClassName('submitted');
        var i;
        for (i=0; i < submittedItems.length; i++) {
            submittedItems[i].style.display = 'none';
        }
    }
    if (featured) {
        var featuredItems = document.getElementsByClassName('featured');
        var i;
        for (i=0; i < featuredItems.length; i++) {
            featuredItems[i].style.display = null;
        }
    }
    // !featured case already taken care of by !approved
}
function pageLoad() {
    document.getElementById('pending-checkbox').checked = true;
    document.getElementById('approved-checkbox').checked = true;
    document.getElementById('feedback-checkbox').checked = true;
    document.getElementById('featured-checkbox').checked = true;
}

function eraseText() {
    document.getElementById("feedback-form").value = "";
}

function badgeSubmitted(index) {
    badgeClicked(index);
    document.getElementsByClassName('tag '+index.toString())[0].value='true';
}

$('.clickable-row').click(function() {
    var id = this.classList[2];
    console.log(id);
    window.location = "/draft/" + id.toString();
    console.log(document.getElementById('draft-alert'));
    document.getElementById('draft-alert').style.display ='block';
});

var searchBar = document.getElementById("searchBar");
if (searchBar) {
  searchBar.addEventListener("input", searchBy, false);
}

function searchBy() {
  const text = searchBar.value.toLowerCase();
  var allProjects = document.getElementsByClassName('project');
  for (var i = 0; i < allProjects.length; i++) {
    const projectName = allProjects[i].getElementsByClassName('card-title')[0].textContent;
    const projectDevelopers = allProjects[i].getElementsByClassName('text-muted')[0].textContent;
    if (projectName.toLowerCase().indexOf(text) >= 0 ||
        projectDevelopers.toLowerCase().indexOf(text) >= 0) {
      allProjects[i].classList.remove('d-none');
    } else {
      allProjects[i].classList.add('d-none');
    }
  }
}
