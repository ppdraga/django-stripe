const initForm = (form, data) => {
    form.html(data.form_html);
    form.find('[name="date"]').datepicker({format: 'mm.dd.yyyy', uiLibrary: 'bootstrap4'});
};

$(function () {

    $('#add-button').on('click', function (e) {
        let modal = $(this).parents('.modal').first();
        let form = modal.find('form');
        $.post(form.attr('action'), form.serialize(), data => {
            if (data.form_is_valid) {
                $('#catalog').html(data.products_html);
                modal.modal('toggle');
            }
            else {
                initForm(form, data)
            }
        });
    });
    $('#Modal').on('show.bs.modal', function (e) {
        let modal = $(this);
        let form = modal.find('form');
        $.get(form.attr('action'), data => {
            initForm(form, data)
        });
    });

});