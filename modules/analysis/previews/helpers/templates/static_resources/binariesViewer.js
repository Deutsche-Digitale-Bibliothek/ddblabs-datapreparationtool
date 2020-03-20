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
$(document).ready(function() {

  if(jsPageName === "detailview"){

    if(navigator.appName.indexOf("Internet Explorer") === -1){
      var mediaQuery = window.matchMedia( "(min-width: 530px)" );
    }

    var currentTab = function(el) {
      $("p.tab").removeClass("current-tab");
      $(el).addClass("current-tab");
    };

    var hideErrors = function() {
      $("div.binary-viewer-error").addClass("off");
      $("div.binary-viewer-flash-upgrade").addClass("off");
    };

    var jwPlayerSetup = function(content,poster){
      if ($("#binary-viewer").length === 0) {
        return;
      }
      $(".viewer-icon").parent().addClass("off");
      $("#binary-viewer").append('<div id="jwplayer-container"></div>');
      var w = 440;
      var h = 320;
      var mediaQueryMatches = 1;
      if(navigator.appName.indexOf("Internet Explorer") === -1){
        mediaQueryMatches = mediaQuery.matches;
      }
      if (!mediaQueryMatches) {
        w = 278;
        h = 200;
      }
      $.initializeJwPlayer("jwplayer-container", content, poster, w, h, function() {
        if ($.browser.msie && this.getRenderingMode() === "html5") {
          $("#binary-viewer").find("[id*='jwplayer']").each(function() {
            $(this).attr("unselectable", "on");
          });
        }
      }, function() {
        if ($("#jwplayer-container")) {
          $("#jwplayer-container").remove();
        }
        if ($("#jwplayer-container_wrapper")) {
          $("#jwplayer-container_wrapper").remove();
        }
        if ($("#jwplayer-container").attr("type") === "application/x-shockwave-flash") {
          $("binary-viewer-flash-upgrade").removeClass("off");
        } else {
          $("div.binary-viewer-error").removeClass("off");
        }
      });
    };

    var updatePreview = function(gallerydiv) {
      var a = gallerydiv.find("ul").children('li').eq(0).children('a');
      var previewUri = $(a).attr("href");
      var previewHref = $(a).attr("data-content");
      var type = $(a).attr("data-type");
      var title = $(a).attr("title");
      var title_text = $(a).attr("title");
      var title_tooltip = $(a).attr("title");
      var author = $(a).attr("data-author");
      var rights = $(a).attr("data-rights");

      // limited to 200 characters
      title_text = $.cutoffStringAtSpace(title, 200);

      // The tooltip of the title should be limited to 270 characters
      title_tooltip = $.cutoffStringAtSpace(title, 270);

      // The text and the tooltip of the author should be limited to 270
      // characters
      author = $.cutoffStringAtSpace(author, 270);

      // The text and the tooltip of the rights should be limited to 270
      // characters
      rights = $.cutoffStringAtSpace(rights, 270);

      hideErrors();
      if(type === "image"){
        if($("#jwplayer-container")) {
          $("#jwplayer-container").remove();
        }
        if($("#jwplayer-container_wrapper")) {
          $("#jwplayer-container_wrapper").remove();
        }
        $(".viewer-icon").parent().addClass("off");
        $(".previews").each(function() {
          if($(this).attr("href") === previewHref) {
            $(this).parent().removeClass("off");
            return false;
          } else {
              $(this).parent().appendTo($("#previews-list"));
          }
        });
        $(".no-previews").each(function() {
          if ($(this).find("img").attr("src") === previewUri) {
            $(this).parent().removeClass("off");
            return false;
          } else {
            $(this).parent().appendTo($("#previews-list"));
          }
        });
        $(".pdf-previews").each(function() {
          if ($(this).attr("href") === previewHref) {
            $(this).parent().removeClass("off");
            return false;
          } else {
            $(this).parent().appendTo($("#previews-list"));
          }
        });
      } else if (type === "video" || type === "audio") {
        jwPlayerSetup(previewHref,previewUri);
      }
      $("div.binary-title span").text(title_text);
      $("div.binary-title").attr("title", title_tooltip);

      $("div.binary-author span").text(author);
      $("div.binary-author").attr("title", author);

      $("div.binary-rights span").text(rights);
      $("div.binary-rights").attr("title", rights);
    };

    var createGallery = function(el) {
      var img = 3;
      var mediaQueryMatches = 1;
      if(navigator.appName.indexOf("Internet Explorer") === -1){
        mediaQueryMatches = mediaQuery.matches;
      }
      if (!mediaQueryMatches) {
        img = 2;
      }
      el.carouFredSel({
        circular: false,
        infinite: false,
        width: 435,
        align: false,
        height: 96,
        items: {
          visible: img,
          minimum: 1
        },
        scroll: {
          items: img,
          fx: "fade"
        },
        auto: false,
        prev: ".slide-viewer .btn-prev",
        next: ".slide-viewer .btn-next"
      });
      if(el.find('li').size()<4) {
        $(".slide-viewer .btn-next").addClass("disabled");
        $(".slide-viewer .btn-next").attr("disabled", true);
      } else {
        $(".slide-viewer .btn-next").attr("disabled", false);
      }
    };

    $(function() {
      var totImages = $(".gallery-images li").size();
      var totVideos = $(".gallery-videos li").size();
      var totAudios = $(".gallery-audios li").size();
      var currentGallery = "";
      if (totImages > 0) {
        currentGallery = "images";
        if (totImages > 1) {
          $("div.tabs").addClass("fix");
        }
      } else if (totVideos > 0) {
        currentGallery = "videos";
        if (totVideos > 1) {
          $("div.tabs").addClass("fix");
        }
      } else if (totAudios > 0) {
        currentGallery = "audios";
        if (totAudios > 1) {
          $("div.tabs").addClass("fix");
        }
      }
      if (currentGallery) {
        currentTab($("p."+currentGallery));
        $("div."+currentGallery).show();
        $(".tab").addClass('show-divider');
        updatePreview($("div."+currentGallery));
        createGallery($(".gallery-"+currentGallery));
      }
    });

    $(".slide-viewer .btn-prev").click(function() {
      if (!$(this).hasClass("disabled")) {
        $(this).addClass("disabled");
        setTimeout(function() {
          $(this).removeClass("disabled");
        }, 500);
      }
    });
    $(".slide-viewer .btn-next").click(function() {
      if (!$(this).hasClass("disabled")) {
        $(this).addClass("disabled");
        setTimeout(function() {
          $(this).removeClass("disabled");
        }, 500);
      }
    });
    $("p.images").click(function() {
      var tab = $("div.images");
      if (tab.find("li").size() === 0) {
        return false;
      }
      currentTab(this);
      $("div.scroller").hide();
      tab.show();
      createGallery($(".gallery-images"));
      updatePreview(tab);
      $("#binary-viewer").addClass("img-binary");
    });
    $("p.videos").click(function() {
      var tab = $("div.videos");
      if (tab.find("li").size() === 0) {
        return false;
      }
      currentTab(this);
      $("div.scroller").hide();
      tab.show();
      createGallery($(".gallery-videos"));
      updatePreview(tab);
      $("#binary-viewer").removeClass("img-binary");
    });
    $("p.audios").click(function() {
      var tab = $("div.audios");
      if (tab.find("li").size() === 0) {
        return false;
      }
      currentTab(this);
      $("div.scroller").hide();
      tab.show();
      createGallery($(".gallery-audios"));
      updatePreview(tab);
      $("#binary-viewer").removeClass(".img-binary");
    });
    $(".previews").click(function(e) {
      e.preventDefault();
      $.fancybox($(".previews"),
                  {
                    'padding' : 0,
                    'closeBtn' : false,
                    'overlayShow' : true,
                    'openEffect' : 'fade',
                    'closeEffect' : 'fade',
                    'prevEffect' : 'fade',
                    'nextEffect' : 'fade',
                    'tpl' : {
                      wrap : '<div class="fancybox-wrap" tabIndex="-1"><div class="fancybox-skin"><div class="fancybox-toolbar">'
                        + '<span title="' + messages.apd.Close() + '" class="fancybox-toolbar-close" onclick="$.fancybox.close();"></span>'
                        +'<span class="fancybox-toolbar-title">'
                        + $("div.binary-title span").text()
                        + '</span><br><div class="fancybox-pagination"><span></span></div></div>'
                        + '<div class="fancybox-outer"><div class="fancybox-inner"><div class="fancybox-click-nav" onclick="$.fancybox.prev();"><div class="fancybox-nav"><span title="Previous" class="fancybox-prev" onclick="$.fancybox.prev();"></span></div></div><div class="fancybox-click-nav right" onclick="$.fancybox.next();"><div class="fancybox-nav"><span title="Next" class="fancybox-next" onclick="$.fancybox.next();"></span></div></div></div></div></div></div>',
                      prev : '',
                      next : ''
                    },
                    'afterLoad' : function() {
                      var title = $.cutoffStringAtSpace($(this.element).attr('data-caption'), 150);
                      var position = $(this.element).attr('data-pos') + ' '
                          + ($("#previews-list li").size() - $(".no-previews").length);
                      $("span.fancybox-toolbar-title").text(title);
                      $("div.fancybox-pagination span").text(position);
                    }
                  });
      if (($('#previews-list li').size() - $(".no-previews").length) === 1) {
        $('.fancybox-pagination').addClass("off");
        $('.fancybox-click-nav').attr('onclick', "");
        $('.fancybox-nav').remove();
      }
      return false;
    });
    $(".show-lightbox").click(function(e) {
      e.preventDefault();
      $(".previews").trigger( "click" );
      return false;
    });
    $("a.group").click(function(e) {
      e.preventDefault();
      var previewUri = $(this).attr("href");
      var previewHref = $(this).attr("data-content");
      var type = $(this).attr("data-type");
      var title = $(this).attr("title");
      var author = $(this).attr("data-author");
      var rights = $(this).attr("data-rights");
      hideErrors();
      if (type === "image") {
        if ($("#jwplayer-container")) {
          $("#jwplayer-container").remove();
        }
        if ($("#jwplayer-container_wrapper")) {
          $("#jwplayer-container_wrapper").remove();
        }
        $(".viewer-icon").parent().addClass("off");
        $(".previews").each(function() {
          if ($(this).attr("href") === previewHref) {
            $(this).parent().removeClass("off");
            return false;
          } else {
            $(this).closest("li").appendTo($("#previews-list"));
          }
        });
        $(".no-previews").each(function() {
          if ($(this).find("img").attr("src") === previewUri) {
            $(this).parent().removeClass("off");
            return false;
          } else {
            $(this).closest("li").appendTo($("#previews-list"));
          }
        });
        $(".no-external-link-icon").each(function() {
          if ($(this).find("img").attr("src") === previewUri) {
            $(this).parent().removeClass("off");
            return false;
          } else {
            $(this).closest("li").appendTo($("#previews-list"));
          }
        });
      } else {
        jwPlayerSetup(previewHref, previewUri);
      }
      // title limited to 200 characters
      var title_text = $.cutoffStringAtSpace(title, 200);
      $("div.binary-title span").text(title_text);
      $("div.binary-title").attr("title", title);
      $("div.binary-author span").text(author);
      $("div.binary-author").attr("title", author);
      $("div.binary-rights span").text(rights);
      $("div.binary-rights").attr("title", rights);
      return false;
    });
  }
});