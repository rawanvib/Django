 $('#id_special_price_from').datepicker({
    format: 'yyyy-mm-dd',
    });
    $('#id_special_price_to').datepicker({
    format: 'yyyy-mm-dd',
    });



 $(function () {
    //Initialize Select2 Elements
    $('.select2').select2()

    //Initialize Select2 Elements
    $('.select2bs4').select2({
      theme: 'bootstrap4'
    })

    $( '#datepicker' ).datepicker()

    });

    $('.formset_row').formset({
    addText: '<button class ="btn btn-primary">+</button>',
    deleteText: '<button class ="btn btn-danger">-</button>',
    prefix: 'product_image',
    });

    $('.formset_row2').formset({
    addText: '<button class ="btn btn-primary">+</button>',
    deleteText: '<button class ="btn btn-danger">-</button>',
    prefix: 'productattributeassoc_set',
    });

    $(document).on('change',".p-id-changed",function () {
      var $this = $(this)
      var url = $("#ProductAttributeAssocForm").attr("data-attribute-url");  // get the url of the `load_cities` view
      var product_attribute_id = $(this).val();  // get the selected country ID from the HTML input

      $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'product_attribute_id': product_attribute_id       // add the country id to the GET parameters
        },
        success: function (data) {
          $this.closest('td').next().find('.p-value-changed').html(data)
        }
      });


});

