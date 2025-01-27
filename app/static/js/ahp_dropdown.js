function updateDisabledOptions() {
    // seleciona os dropdown Criterion e Alternatives
    const selects = document.querySelectorAll('select[name^="criterion_"], select[name^="alternative_"]');
    const selectedValues = [];

    // busca os valores selecionados em todos os select
    selects.forEach(function(select) {
        const selectedOption = select.options[select.selectedIndex];
        if (selectedOption && selectedOption.value) {
            selectedValues.push(selectedOption.value);
        }
    });

    // deixa todas opcoes enabled
    selects.forEach(function(select) {
        const options = select.querySelectorAll('option');
        options.forEach(function(option) {
            option.disabled = false;
        });
    });

    // faz opcoes selecionadas ficarem disabled em todos dropdown
    selects.forEach(function(select) {
        const options = select.querySelectorAll('option');
        options.forEach(function(option) {
            if (selectedValues.includes(option.value) && option.value !== '') {
                option.disabled = true;
            }
        });

        // mantem a opcao selecionada enabled no seu proprio dropdown
        const selectedOption = select.options[select.selectedIndex];
        if (selectedOption && selectedOption.value) {
            selectedOption.disabled = false;
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const selects = document.querySelectorAll('select[name^="criterion_"], select[name^="alternative_"]');
    selects.forEach(function(select) {
        select.addEventListener('change', updateDisabledOptions);
    });

    // chama funcao para desabilitar as opcoes preselecionadas
    updateDisabledOptions();
});