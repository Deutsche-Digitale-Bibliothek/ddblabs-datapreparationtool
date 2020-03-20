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

//TODO review if it has to be a global variable
var stateManager = stateManager || new de.ddb.apd.search.StateManager();
var urlManager = urlManager || new de.ddb.apd.search.UrlManager();

$(document).ready(
  function() {
    //TODO Create functionality to update this variables when the page is resize.
    de.ddb.apd.facetSelectedVar = $.isMobile() ? '#facets-selected-container-phone' : '#facets-selected-container';
    de.ddb.apd.deviceVar = $.isMobile() ? '#filter-objects-flyout ' : '';

    var initFromUrl = function() {
      var selFilterValues = stateManager.getFilters();
      var selFacetValues = stateManager.getAllFacets();
      if ( (selFilterValues.length>0) || (selFacetValues.length>0) ) {
          var json = null;
          var searchParameters = de.ddb.common.search.readCookie("searchParameters" + jsContextPath);
          if (searchParameters != null && searchParameters.length > 0) {
              searchParameters = searchParameters.substring(1, searchParameters.length - 1);
              searchParameters = searchParameters.replace(/\\"/g, '"');
              json = $.parseJSON(searchParameters);
              if(json && json["resetFilters"] === 1) {
                  $('#reset-checkbox').prop("checked",true);
              }
          }
          $('.reset-filters').removeClass("off");

      }
    };

    /* Only unsets resetFilter selection in cookie. */
    var unSelectResetAllFilters = function () {
        var paramsArray = [];
        paramsArray.push(['resetFilters', 0]);
        de.ddb.common.search.setSearchCookieParameter(paramsArray);
        if(!( (stateManager.getFilters().length>0) || (stateManager.getAllFacets().length>0) )) {
        $('.reset-filters').fadeOut();
        }
    };

    /* Init the reset checkbox everyime it is going to make a fresh appearance. Init = set resetFilters cookie to 0 and checkbox unchecked */
    var initResetAllFilters = function() {
        unSelectResetAllFilters();
        if($('#reset-checkbox').prop("checked")) {
            $('#reset-checkbox').prop("checked",false);
        }
        $('.reset-filters').fadeIn();
        $('.reset-filters').removeClass("off");
    };

    var initOnLoad = function() {
      initFromUrl();
      var stateChangeCallback = function() {
        var selFilterValues = stateManager.getFilters();
        var selFacetValues = stateManager.getAllFacets();
        if ( (selFilterValues.length>0) || (selFacetValues.length>0) ){
          if($('.reset-filters').is(":hidden")) {
            initResetAllFilters();
          }
         }
        else if($('.reset-filters').is(":visible")) {
          unSelectResetAllFilters();
        }
       };
        stateChangeCallback.origin = "objectSearch.js";
        stateManager.addStateChangeCallback(stateChangeCallback);
    };

    /* Only sets resetFilter selection in cookie. In actual filters are reset only after search button is clicked */
    var selectResetAllFilters = function() {
        var paramsArray = [];
        paramsArray.push(['resetFilters', 1]);
        de.ddb.common.search.setSearchCookieParameter(paramsArray);
    };

    var init = function() {
      $('#search-objects').click(function(event) {
        event.preventDefault();
        searchAction($('#query').val());
      });

      $('#query').keypress(function(e) {
        if(e.which === 13 && $('#query').is(':focus')) {
          searchAction($('#query').val());
        }
      });

      //Mobile
      $('#index-search-objects').click(function(event) {
        event.preventDefault();
        searchAction($('#index-query-phone').val());
      });

      /* handle reset filters checkbox*/
      $('#reset-checkbox').change(function() {
        if($(this).attr('name') === "reset-checkbox") {
          var resetCb = $(this);
            if(resetCb.prop('checked') ) {
              selectResetAllFilters();
            } else {
                unSelectResetAllFilters();
              }
        }
      });

      initOnLoad();

    };

    //TODO boz: This method needs refactoring.
    // Most of this code should be done automatically by the filterWidgetController and the facetscontroller inside initOnLoad.
    var resetAllFilters = function () {

      //1) Show hidden dropdownlist element again
      selectedFilter= $(".dropdown-menu").find(".off");
      $.each(selectedFilter, function(key, ele) {
        $(ele).removeClass("off");
      });

      //2) Remove the selected filters and facets from the filter and facet bar
      $(".filter").remove();
      $(de.ddb.apd.facetSelectedVar).empty();

      if($(de.ddb.apd.deviceVar + '.media-filter').prop("checked")) {
        $(de.ddb.apd.deviceVar + '.media-filter').prop('checked', false);
      }

      //3) Reset all filters from url and load the changed url
      stateManager.resetFilters();

      //5) Remove the reset-filters checkbox
      if($('#reset-checkbox').prop("checked")) {
        $('#reset-checkbox').prop("checked",false);
      }
      unSelectResetAllFilters();
    };

    // If the parameter "resetFilters" equals 1 than invokes the filter reset
    var checkResetAllFilters = function() {
      var json = null;
      var searchParameters = de.ddb.common.search.readCookie("searchParameters" + jsContextPath);
      if (searchParameters != null && searchParameters.length > 0) {
        searchParameters = searchParameters.substring(1, searchParameters.length - 1);
        searchParameters = searchParameters.replace(/\\"/g, '"');
        json = $.parseJSON(searchParameters);
        if (json && json["resetFilters"] === 1) {
          resetAllFilters();
        }
      }
    };

    /**
     * Set and execute the query
     */
    function searchAction(searchTerm) {
      checkResetAllFilters();
      stateManager.setQuery(searchTerm, false);
      stateManager.setOffset("0", false);
      stateManager.removeSort(false);
      if (jsPageName !== "objectsList") {
        // if the browser doesn't support the push state
        if (!window.history || !history.pushState) {
          var currObjInstance = this;
          var baseUrl = $('#search-objects').attr("href").split('?')[0];
          var currentUrl = currObjInstance.urlManager.getUrl();
          currentUrl = currObjInstance.urlManager.createURLwithQueryParameter(currentUrl, "query", searchTerm, baseUrl);
          $('#search-objects').attr("href", currentUrl);
        }
        window.location = $('#search-objects').attr('href');
      }
    };

    init();
  });
