///**
// * built according to "Revealing Module Pattern (Public & Private)"
// * http://enterprisejquery.com/2010/10/how-good-c-habits-can-encourage-bad-javascript-habits-part-1/
// */

var MAP_DIV = 'institution-item-map';

// only initialize map once, then remember in this variable
var mapInitialized = false;

var map;

var InstitutionsMapAdapter = (function() {
  'use strict';

  // for public properties. avoid the reserved keyword "public"
  var Public = {};
  //
  Public.drawInstitution = function(mapDiv, lang, lon, lat) {
    map = new DDBMap();
    map.displayMarker({
      "rootDivId" : MAP_DIV
    }, lang, lon, lat, 16);
  };

  return Public;

})(jQuery);

function mapSetup() {
  jsLongitude = $("div.location").attr('data-lon');
  jsLatitude = $("div.location").attr('data-lat');

  if ($("#institution-item-map").length > 0){
    InstitutionsMapAdapter.drawInstitution(MAP_DIV, jsLanguage, jsLongitude, jsLatitude);
  }

  return;
};

$(document).ready(function() {
  if (jsPageName === "institutionDetail" ) {
    document.title = $('.institution-name').text() +" - " + messages.apd.ArchivportalD();
  }
  mapSetup();
});