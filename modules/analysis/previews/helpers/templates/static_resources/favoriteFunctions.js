/*
 * Copyright (C) 2014 FIZ Karlsruhe
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

de.ddb.apd.activateFavorites = function() {

  /**
   * Add a button click handler to all favorite buttons which object id is not yet stored in the list of favorites.
   *
   * @param objectIds list of the object id's from all favorite buttons on the current page
   */
  addClickHandler = function(objectIds) {
    $(".add-to-favorites").each(function() {
      var objectData = extractObjectData($(this));
      if ($.inArray(objectData.id, objectIds) >= 0) {
        disableFavorite($(this));
      }
      else {
        $(this).click(function() {
          addFavorite(objectData.id, null, objectData.type);
          disableFavorite($(this));

          var confirmButton = $("#add-to-favorites-confirm");
          if (confirmButton.length > 0) {
            confirmButton.click(function(event) {
              event.preventDefault();
              if($("#favorite-folders").val()) {
                $.each($("#favorite-folders").val(), function(index, folderId) {
                  addFavorite(objectData.id, folderId, objectData.type);
                });
              }
              $("#favorite-confirmation").modal("hide");
            });
            $("#favorite-confirmation").modal("show");
            $.get(jsContextPath + "/apis/merklisten", function(folders) {
              if (folders.length > 1) {
                $("#favorite-folders").empty();
                $.each(folders, function(index, folder) {
                  if (!folder.isMainFolder) {
                    // show select box with all folder names
                    var selectEntry = "<option value=" + folder.folderId + ">"
                      + folder.title.charAt(0).toUpperCase() + folder.title.slice(1)
                      + "</option>";
                    $("#favorite-folders").append(selectEntry);
                  }
                });
              }
            });
          }
          else {
            $("#simple-favorite-confirmation").modal("show");
          }
        });
      }
    });
  };

  /**
   * Add an object to the list of favorites.
   *
   * @param id object id
   * @param folderId folder id
   * @param type object type
   */
  addFavorite = function(id, folderId, type) {
    $.ajax({
      type : "POST",
      dataType : 'json',
      async : true,
      url : jsContextPath + "/apis/merkliste/" + id + "?&reqObjectType=" + type
        + (folderId ? "&folderId=" + folderId : ""),
      statusCode : {
        201 : function() {
          $.get(jsContextPath + "/apis/merkliste", function(data) {
            $(".merkliste-number").html(data.length);
          });
        }
      }
    });
  };

  /**
   * Check if the result hits are already stored in the list of favorites.
   *
   * @param objectIds list of the object id's from all favorite buttons on the current page
   * @param callback function which will be called with the list of the object id's as parameter
   *
   * @return list of object id's which are already stored in the list of favorites
   */
  checkFavorites = function(objectIds, callback) {
    $.ajax({
      type : "POST",
      url : jsContextPath + "/apis/merkliste/_filter",
      contentType : "application/json",
      data : JSON.stringify(objectIds),
      success : function(favoriteObjectIds) {
        if (callback) {
          callback(favoriteObjectIds);
        }
      }
    });
  };

  /**
   * Disable a favorite button.
   *
   * @param element HTML element which handles the favorite event
   */
  disableFavorite = function(element) {
    element.unbind("click");
    element.addClass("added-to-favorites");
  };

  /**
   * Get the object id and object type from the data attributes of the given HTML element.
   *
   * @param element HTML element which handles the favorite event
   *
   * @return a map with "id" and "type"
   */
  extractObjectData = function(element) {
    var id = $(element).attr("data-iid");
    var type = $(element).attr("data-objecttype");
    var hierarchy = $(element).siblings(".hierarchy-container");
    if (hierarchy.length) {
      id = $(hierarchy).attr("data-iid");
      type = $(hierarchy).attr("data-objecttype");
    }
    return {"id": id, "type": type};
  };

  if (jsLoggedIn === "true") {
    var objectIds = [];

    // collect all object id's on the page
    $(".add-to-favorites").each(function() {
      var objectData = extractObjectData($(this));
      objectIds.push(objectData.id);
    });
    checkFavorites(objectIds, addClickHandler);
  }
};