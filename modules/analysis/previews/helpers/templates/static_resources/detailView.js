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

de.ddb.apd.detail = de.ddb.apd.detail || {};

var stateManager = stateManager || new de.ddb.apd.search.StateManager();

$(document).ready(function() {
  $('#fields').glossary(jsGlossaryUrl, {
    excludetags: ['a']
  });

  if (jsPageName === 'detailview') {
    document.title = $(".object-details-title").text() +" - " + messages.apd.ArchivportalD();

    $(".fields .rights a").attr("target","_blank");

    var socialMediaManager = new SocialMediaManager();
    socialMediaManager.integrateSocialMedia();

    //retrieve and render the siblings for the item
    de.ddb.apd.detail.getSiblings();

    // add to favorites function
    de.ddb.apd.activateFavorites();

    //Set the links in the hierarchie which depends on the search state
    de.ddb.apd.detail.updateHierarchyLinks();

    //add eye icon on the last item of the hierarchy if it is a link
    var hierarchyLis = $('#hiearchy-navigation .span9 li');
    //add the eyeicon on the last element of the hierarchy if it is an anchor
    if ($(hierarchyLis.get(hierarchyLis.length-1)).children('a').length) {
      var eyeIcon = $(document.createElement('i'));
      eyeIcon.addClass('apd-icon apd-icon-view-green');
      $(hierarchyLis.get(hierarchyLis.length-1)).children('a').append(eyeIcon);
    }

    if(stateManager.getParameters() ) {
      $(".back-to-list").removeClass("off");
    }
  }
});

/**
 * Update the links in the hierarchy container with the search parameters and the corresponding context id
 */
de.ddb.apd.detail.updateHierarchyLinks = function() {
  $(".hierarchy-link").each(function() {

    //TODO Temporal code, APD-773, related with the data problem with the context facet
    var url = jsContextPath + "/objekte";
    var stateParameters = stateManager.getParameters();
    var id = $(this).attr("data-id");
    var type = $(this).attr("data-type");
    var tempContext = stateManager.getContextFacet();
    var tempProviderID = stateManager.getProviderIdFacet();
    var offset = stateManager.getOffset();

    //Check for stateParameters because they are removed if the user change the sibling
    if (stateParameters) {
      stateManager.removeQuery();
      if(type === "institution") {
        if (tempContext) {
          stateManager.removeContextFacet(false, false);
          url += stateManager.getParameters() + "&facetValues%5B%5D=provider_id%3D" + id;

          //Necessary to create the others links of the page, e.g. links "Weiter" "Ende"
          stateManager.setContextFacet(tempContext, false, false);
        //If the state parameters already contains the provider_id, than replace it with the provider_id of the hierarchy
        } else if (tempProviderID){
          url += stateParameters.replace(tempProviderID, id);
        } else {
          url += stateParameters + "&facetValues%5B%5D=provider_id%3D" + id;
        }
      } else {
        if (tempProviderID) {
          stateManager.removeProviderIdFacet(false, false);
          url += stateManager.getParameters() + "&facetValues%5B%5D=context%3D" + id;

        //Necessary to create the others links of the page, e.g. links "Weiter" "Ende"
          stateManager.setProviderIdFacet(tempProviderID, false, false);
        }
        //If the state parameters already contains the context, than replace it with the context of the hierarchy
        else if (tempContext) {
          url += stateParameters.replace(tempContext, id);
        } else {
          url += stateParameters + "&facetValues%5B%5D=context%3D" + id;
        }
      }
    } else {
      if(type === "institution") {
        url += "?facetValues%5B%5D=provider_id%3D" + id;
      } else {
        url += "?facetValues%5B%5D=context%3D" + id;
      }
    }

    url = url.replace("offset=" + offset, "offset=0");

    $(this).attr("href", url);
  });
};

/**
 * Retrieves and renders the siblings for an item via AJAX call.
 */
de.ddb.apd.detail.getSiblings = function() {
  var itemId = $(".container.detailview").data("iid");
  var url = jsContextPath + '/detail/siblings/' + itemId;

  var request = $.ajax({
    type : 'GET',
    dataType : 'json',
    async : true,
    url : url,
    beforeSend: function(){
      $(".container.detailview").find("*").prop("disabled", true);
      $(".small-loader").removeClass("off");
    },
    complete : function() {
      $("#navigation").html(request.responseText);

      $('#siblings-dropdown').change(function() {
        var path = $("#siblings-dropdown").val();
        var linkUrl = location.protocol + "//" + location.host + path;
        window.location = linkUrl;
      });

      $(".container.detailview").find("*").prop("disabled", false);
      $(".small-loader").addClass("off");
    }
  });
};
