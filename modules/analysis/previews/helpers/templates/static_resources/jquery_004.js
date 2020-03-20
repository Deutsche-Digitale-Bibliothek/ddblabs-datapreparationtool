/**
 * Plugin: jquery.zGlossary
 * 
 * Version: 1.0.2
 * (c) Copyright 2011-2013, Zazar Ltd
 * 
 * Description: jQuery plugin to find and display term definitions in HTML text
 * 
 * History:
 * 1.0.2 - Added show once option
 * 1.0.1 - Correct mistype to _addTerm function (Thanks Aldopaolo)
 * 1.0.0 - Initial release
 *
 **/

(function($){
  $.fn.glossary = function(url, options) {
    // Set plugin defaults
    var defaults = {
      ignorecase: false,
      tiptag: 'h6',
      excludetags: [],
      linktarget: '_self',
      showonce: false
    };  
    var options = $.extend(defaults, options); 
    var id = 1;

    // Functions
    return this.parent().each(function(i, e) {

      // Ensure any exclude tags are uppercase for comparisons
      $.each(options.excludetags, function(i,e) { options.excludetags[i] = e.toUpperCase(); });

      // Function to find and add term
      var _addTerm = function(e, term, type, def, synonyms) {
        var patfmt = term;
        var skip = 0;
        
        // Check the element is a text node
        if (e.nodeType == 3) {
          // Case insensistive matching option
          if (options.ignorecase) {
            var pos = e.data.toLowerCase().indexOf(patfmt.toLowerCase());
          } else {
            var pos = e.data.indexOf(patfmt);
          }
          
          
          //Check if one of the synonyms matches in the list and link to the term
          if (typeof synonyms !== 'undefined' && synonyms.length > 0) {
            for (var i=0; i < synonyms.length; i++) {

              if (e.data.toLowerCase().indexOf(synonyms[i].toLowerCase())>=0){
                pos = e.data.toLowerCase().indexOf(synonyms[i].toLowerCase());
                patfmt=synonyms[i];

              }
            }
          }
          // Check if the term is found
          if (pos >= 0) {

        	  //Needed as I want full words and not attached words to be anchored
        	  var nextCh = e.data.charAt(patfmt.length+pos);

        	  //This Regexpression guarantees that the end of the term found creates a word. 
        	  var endChar = new RegExp(/^\s|\]|\.$/);
        	  // Check for excluded tags
        	  if (jQuery.inArray($(e).parent().get(0).tagName,options.excludetags) > -1) {
        	    
            } else if ((endChar.test(nextCh))){
              // Create link element
              var spannode = document.createElement('a');
              spannode.className = 'glossaryTerm';

              if (type == '0') {
                // Popup definition
                spannode.id = "glossaryID" + id;
                spannode.href = jsContextPath +"/info/glossar#" + term;
                spannode.className = 'glossaryTerm';
                spannode.setAttribute("data-toggle","popover");
                spannode.setAttribute("data-original-title", term);
                spannode.setAttribute("data-content", def);
                spannode.setAttribute("data-placement","right");
                spannode.setAttribute("data-trigger","hover");
              } else if (type == '1') {
                // Anchor definition
                spannode.title = 'Click to look up \''+  term;
                term = term.replace(/ /g, "_");
                spannode.href = jsGlossaryPageUrl+'#'+term;
                spannode.target = options.linktarget;
              }
              var middlebit = e.splitText(pos);
              var endbit = middlebit.splitText(patfmt.length);
              var middleclone = middlebit.cloneNode(true);

              spannode.appendChild(middleclone);
              middlebit.parentNode.replaceChild(spannode, middlebit);

              skip = 1;
              id += 1;
            }
          }
        }
        else if (e.nodeType == 1 && e.childNodes && !/(script|style)/i.test(e.tagName) && e.className!="modal hide fade") {
          // Search child nodes
          for (var i = 0; i < e.childNodes.length; ++i) {

            var ret = _addTerm(e.childNodes[i], term, type, def,synonyms);

            // If term found and show once option go to next term
            if (options.showonce && ret == 1) {
              i = e.childNodes.length;
              skip = 1;
            } else {
              i += ret;
            }
          }
        }

        return skip;
      };

      var correctJson = function( json ) {
        $.each(json, function(id, item) {
            if(item && item.definition) {
                var regex = new RegExp("\\[\\[(.*?)\\]\\]","g")
                var res = item.definition.match(regex);
                var i = 0;
                while(res && res.length > i) {
                    var match = res[i]
                    var j = match.indexOf("|");
                    if(j>0) {
                        var subStr = match.substring(2, j);
                        item.definition = item.definition.replace(match,subStr);
                    }
                    i++;
                }
            }
        });
        return json;
    };
      // Get glossary list items
      $.ajax({
        type: 'GET',
        url: url,
        dataType: 'json',
        success: function(data) {

          if (data) {
            var jsonData = correctJson(data);
            var count = jsonData.length;
            for (var i=0; i<count; i++) {
              // Find term in text
              var item = jsonData[i];
              var term = item.term.replace(/\s/g, '_');
              _addTerm(e, term, item.type, item.definition, item.synonyms);
            }
            $.initWordsDefinitions();
          }
        },
        error: function() {}
      });

    });
  
  };

  // Glossary tip popup
  var glossaryTip = function() {}

  $.extend(glossaryTip.prototype, {
    setup: function(){

      if ($('#glossaryTip').length) {
        $('#glossaryTip').remove();
      }
      glossaryTip.holder = $('<div id="glossaryTip" style="max-width:260px;"><div id="glossaryClose"></div></div>');
      glossaryTip.content = $('<div id="glossaryContent"></div>');

      $('body').append(glossaryTip.holder.append(glossaryTip.content));
    },

    show: function(content, event){

      glossaryTip.content.html(content);

      // Display tip at mouse cursor
      var x = parseInt(event.mouse_event.pageX) + 15
      var y = parseInt(event.mouse_event.pageY) + 5
      glossaryTip.holder.css({top: y, left: x});

      // Display the tip
      if (glossaryTip.holder.is(':hidden')) {
        glossaryTip.holder.show();
      }

      // Add click handler to close
      glossaryTip.holder.bind('click', function(){
        glossaryTip.holder.stop(true).fadeOut(200);
        return false;
      });
      
    }

  });

  $.glossaryTip = function(content, event) {
    var tip = $.glossaryTip.instance;

    if (!tip) { tip = $.glossaryTip.instance = new glossaryTip(); }

    tip.setup();
    tip.show(content, event);

    return tip;
  }

})(jQuery);
