/* global ContentEditor, django */
(function($) {
  $(document).on('content-editor:ready', function() {
    var buttons = [
      ['_header', '<i class="fas fa-heading"></i>'],
      ['_button', '<i class="fas fa-square"></i>'],
      ['_divider', '<i class="fas fa-horizontal-rule"></i>'],
      ['_richtext', '<i class="fas fa-pencil-alt"></i>'],
      ['_image', '<i class="fas fa-image"></i>'],
      ['_external', '<i class="fas fa-film"></i>'],
      ['_html', '<i class="fas fa-code"></i>'],
      ['_formplugin', '<i class="fas fa-poll"></i>'],

      ['_gallery', '<i class="fas fa-images"></i>'],
      ['_slide', '<i class="fas fa-image"></i>'],
      ['_snippet', '<i class="fas fa-cog"></i>'],
      ['_table', '<i class="fas fa-table"></i>'],
      ['_team', '<i class="fas fa-users"></i>'],
      ['_person', '<i class="fas fa-user"></i>'],
      ['_eventplugin', '<i class="fas fa-calendar"></i>'],
      ['_articleplugin', '<i class="fas fa-newspaper"></i>'],

    ]

    for (var i = 0; i < buttons.length; ++i) {
      ContentEditor.addPluginButton('pages' + buttons[i][0], buttons[i][1])
      ContentEditor.addPluginButton('blog' + buttons[i][0], buttons[i][1])
      ContentEditor.addPluginButton('events' + buttons[i][0], buttons[i][1])
    }

    const updateCollapseListeners = function() {
      $('.toggle-inline-fieldset').not('.toggle-listener-installed').on('click', function(){
        const cardHeader = this.parentElement.parentElement;
        const collapse = cardHeader.nextElementSibling;
        collapse.classList.toggle('show');
      });
      $('.toggle-inline-fieldset').addClass('toggle-listener-installed');
    };


    const callback = function(mutationsList, observer) {
      applySelect2();
      updateCollapseListeners();
    };


    const config = {
      attributes: false,
      childList: true,
      subtree: false
    };

    const observer = new MutationObserver(callback);

    observer.observe(document.getElementsByClassName('order-machine')[0], config);

    updateCollapseListeners();

    $('.control-unit > select').select2({theme: "classic"}).on("change", function () {
      ContentEditor.addContent(this.value);
      console.log(this.value);
      this.value = "";
    });

  });

})(django.jQuery)
