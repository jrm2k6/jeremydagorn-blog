/* global $, document, window, CONFIG, removeCurrentActiveClass*/
'use strict';


var _cells = [];
var _projects;
var listLayout;

function Project() {}

Project.prototype = {
    
    init : function(obj) {
        this.id = obj.id;
        this.title = obj.title;
        this.description = obj.filename;
        this.status = obj.status;
        this.technologies = obj.technologies;
        return this;
    },

    getStatusAsString : function() {
        var STATUS = ["DONE", "IN-PROGRESS", "IN-MY-MIND"];
        var status = this.status-1;
        
        if (this.status !== undefined) {
            if (status >= STATUS.length) throw new Error("Status id needs to be lower than the length of array STATUS." +
                "Have you referenced your new status in this array?");
            return STATUS[status];
        }
    },

    getGlyphiconNameFromStatus : function() {
        var STATUS = ["glyphicon-ok", "glyphicon-pencil"];
        var status = this.status-1;
        if (this.status !== undefined) {
            if (status >= STATUS.length) throw new Error("Status id needs to be lower than the length of array STATUS." +
                "Have you referenced your new status in this array?");
            return STATUS[status];
        }
    },

    getTruncatedDescription : function() {
        if (this.description.length > 150) {
            return this.description.substring(0, 146) + "...";
        } else {
            return this.description;
        }
    }
};

function ListLayout() {}

ListLayout.prototype = {
    createContainerProject : function(i) {
        var $container = $('<div>', { id: "container_project_" + i});
        $container.css({"margin-top": "20px"});
        return $container;
    },

    createProjectTitleDiv : function(i, project) {
        var $div = $('<div>', { id: "title_" + i, text: project.title});
        $div.css({color: "white", "font-size": "20px"});
        $div.attr("data-status", project.getStatusAsString());
        $div.attr("data-description", project.getTruncatedDescription());
        $div.mouseover(function() {
            $div.css("color", "#e77471");
        });

        $div.mouseout(function() {
            $div.css("color", "white");
        });
        var self = this;
        $div.on("click", function() {
            self.closeOpenItem();
            self.displayProjectDetails(_cells[i], $(this).attr("data-status"));
        });

        return $div;
    },

    closeOpenItem : function(){
        if (this.openItem === undefined) return;

        var id = parseInt(this.openItem.attr("id").split("_")[2], 10);
        var idFullDivs = id + 1;
        
        this.openItem.removeClass("list_layout_detailed_project");

        $("#description_" + idFullDivs).remove();
        $("#technologies_" + idFullDivs).remove();
        $("#status_" + idFullDivs).remove();
        
                var $title = this.openItem.find(">:first-child");
        $title.css("border-bottom", "none");
        
                var shortDescription = $title.attr("data-description");
        var $description = $('<div>', {id: "description_" + id, text: shortDescription});
        $description.addClass("pink-description");
        this.openItem.append($description);

    },

    displayProjectDetails : function(project, statusAsString) {
                var id = project.id - 1;
        var $container = $("#container_project_" + id);

        $("#description_"+ id).remove();
        this.openItem = $container;
        
        $container.addClass("list_layout_detailed_project");

        var $title = $("#title_" + id);
        $title.css({"padding-bottom": "3px", "border-bottom":"1px solid #ffa5d2", "color" : "#e77471"});

        var $description = $('<div>', {id: "description_" + project.id, text: project.description});
        $description.css({"color": "white", "size" : "18px"});
        $container.append($description);

        var $technologies = $('<div>', {id: "technologies_" + project.id, text: project.technologies});
        $technologies.css({"color": "#a1a8a3", "size" : "17px"});
        $container.append($technologies);

        var $status = $('<div>', {id: "status_" + project.id, text: statusAsString});
        $status.css({"color": "#ffa5d2", "size" : "17px"});
        $container.append($status);
    },

    createProjectDescriptionDiv : function(i, project) {
        return $('<div>', {id: "description_" + i, text: project.getTruncatedDescription()}).addClass("pink-description");
    },

    displayProjectsAsList : function(cells) {
        $("#pgrid").css("height", 800);
        $("#listing").attr("data-layout", 1);
    
        
        for (var i=0; i<cells.length; i++) {
            var project = cells[i];
            var $container = this.createContainerProject(i);
            var $divProjectTitle = this.createProjectTitleDiv(i, project);
            var $divProjectDescription = this.createProjectDescriptionDiv(i, project);
            
            $("#pgrid").append($container);
            $container.append($divProjectTitle);
            $container.append($divProjectDescription);
        }
    }
};


function fetchProjects() {
    $.getJSON( "/fetch/projects", function(data) {
            callback(data);
        });
}

function callback(data) {
    for (var i=0; i<data.length; i++) {
        var t = new Project().init(data[i]);
        _cells.push(t);
    }
    
    listLayout = new ListLayout();
    listLayout.displayProjectsAsList(_cells);
}


function clearMainDiv() {
    $("#pgrid").html("");
}

$(window).load(function() {
    removeCurrentActiveClass();
    
        if (window.CONFIG === undefined || !CONFIG.Test) {
        fetchProjects();
    }
});
