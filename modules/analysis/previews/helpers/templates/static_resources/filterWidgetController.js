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

/* Search namespace  */
de.ddb.apd.search = de.ddb.apd.search || {};

//TODO review if it has to be a global variable
var stateManager = stateManager || new de.ddb.apd.search.StateManager();

/**
 * Handles the institutions filter values. Filterv values are stored in the url to support bookmarking and browser
 * history with back/next button.
 */
de.ddb.apd.search.FilterWidgetController = function(filterElement, removeFacetsOnChange) {
  this.removeFacetsOnChange = removeFacetsOnChange;
  this.filterElement = filterElement;
  this.init();
};

/**
 * Extend the prototyp of the FilterWidgetController with jQuery
 */
$.extend(de.ddb.apd.search.FilterWidgetController.prototype, {

  init : function() {
    var self = this;

    // Add functionality to all checkboxes from alphabet filter
    self.filterElement.find("input[type='checkbox']").change(function() {
      var cb = $(this);

      var val = cb.attr('data-value');
      var type = cb.attr('data-type');

      if(cb.is(':checked')) {
        cb.parent().toggleClass("checked", true);
        self.selectFilterItem($(this));
      }
      else {
        cb.parent().toggleClass("checked", false);
        self.unselectFilterItem(type, val);
      }

    });

    // Add functionality to all links from the state and sector list
    var filterValues = self.filterElement.find('a.filter-value');
    filterValues.click(function(event) {
      event.preventDefault();

      self.selectFilterItem($(this));
      $(this).parent().addClass("off");
    });

    // Initialize the filterManager
    var historyCallback = function () {
      self.initOnLoad();
    };
    historyCallback.origin = "FilterWidgetController";

    //Register callback method at the StateManager to handle onLoad
    stateManager.addHistoryCallback(historyCallback);

    self.initOnLoad();
  },

  /**
   *
   */
  initOnLoad : function() {
    var self = this;
    self.resetPage();
    self.initFromUrl();
  },

  /**
   * Resets the state of the filter components
   */
  resetPage : function() {
    var self = this;

    self.filterElement.find(".filter").remove();

    self.filterElement.find('a.filter-value').parent().removeClass("off");

    //Reset all checkboxes
    self.filterElement.find("input[type=checkbox]").prop('checked', false);

    self.filterElement.find('input[type=checkbox]').each(function() {
      this.checked = false;
      var chb = $(this);
      chb.parent().removeClass("checked");
    });
  },

  /**
   * Initialize the filter values from the window url
   */
  initFromUrl : function() {
    var self = this;

    var selFilterValues = stateManager.getFilters();
    if (selFilterValues) {
      $.each(selFilterValues, function(key, filterValue) {

        filterValueDecoded = decodeURIComponent(filterValue).replace(/\+/g, " ");

        var delimiterPos = filterValueDecoded.toString().indexOf("_");
        var name = filterValueDecoded.substring(0, delimiterPos);
        var value = filterValueDecoded.substring(delimiterPos + 1);

        // find the filter checkbox items and trigger a click event
        self.filterElement.find("input[type=checkbox][data-type='" + name + "'][data-value='" + value + "']").trigger('click');

        // find the filter anchor items and trigger a click event
        self.filterElement.find("a.filter-value[data-type='" + name + "'][data-value='" + value + "']").trigger('click');
      });
    }
  },

  /**
   * Handles a filter value selection.
   */
  selectFilterItem : function(filter) {

    var self = this;
    var val = filter.attr('data-value');
    var label = filter.attr('data-label');
    var name = filter.attr('data-type');

    if(name !== "hasItems") {
      var newFilter = self.renderSelectedFilterItem(name, label, val);
      self.filterElement.find('#institution-filter').after(newFilter);
    } else {
      self.filterElement.find("#institution-filter").css("display","block");
    }

    self.initFilterCloseBtn();
    // Check if the value is already available via the stateManager
    if (!stateManager.hasFilter(name, val)) {
      if (self.removeFacetsOnChange) {
        stateManager.removeFacets(false);
      }
      stateManager.setOffset("0", false);
      stateManager.setFilter(name, val);
    }
  },

  /**
   * Handles the unselection of a filter value.
   * Update the window url
   */
  unselectFilterItem : function(filterType, filterValue) {
    var self = this;
    // 1) Remove value from window url
    if (self.removeFacetsOnChange) {
      stateManager.removeFacets(false);
    }
    stateManager.setOffset("0", false);
    stateManager.removeFilter(filterType, filterValue);
    // 2) Deselect alphabet checkbox
    self.filterElement.find("input[type='checkbox']").each(function() {
      var cb = $(this);
      if (cb.attr("data-value") === filterValue) {
        cb.prop('checked', false);
        cb.parent('label').removeClass('checked');
      }
    });
    // 3) Show hidden dropdownlist element again
    var selectedFilter = self.filterElement.find(".filter-value[data-type='" + filterType + "'][data-value='" + filterValue + "']");
    if (selectedFilter) {
      selectedFilter.parent().removeClass("off");
    }
    // 4) Remove the pillbox
    var pillbox = self.filterElement.find(".filter[data-type='" + filterType + "'][data-value='" + filterValue + "']");
    pillbox.remove();
  },

  /**
   * Initialize the logic for the filter close buttons
   */
  initFilterCloseBtn : function() {
    var self = this;

    self.filterElement.find('.filter .dismiss-filter').on('click', function() {
      var val = $(this).parent().attr('data-value');
      var type = $(this).parent().attr('data-type');

      self.unselectFilterItem(type, val);
    });
  },

  /**
   * Renders the html code for a selected filter value
   */
  renderSelectedFilterItem : function(name, label, val) {
    return $('<span class="filter" data-type="' + name + '" data-label="' + label + '" data-value="' + val + '">'
        + label + '<button class="dismiss-filter" type="button">×</button></span>');
  }
});
