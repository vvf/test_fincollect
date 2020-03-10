(function () {
    var $form = document.getElementById('converter-form');
    var $fromSelect = document.getElementById('currency-from');
    var $toSelect = document.getElementById('currency-to');
    var $amountInput = document.getElementById('amount');
    var $resultValueContainer = document.getElementById('result-container');
    var currenciesData = JSON.parse(document.getElementById('currencies-data').innerHTML);
    var calculateRate = function (fromCurrency, toCurrency) {
        if (!currenciesData[fromCurrency] || !currenciesData[toCurrency]) {
            console.error("No data for some currency of ", fromCurrency, toCurrency);
            return;
        }
        var rubFrom = currenciesData[fromCurrency].rub;
        var rubTo = currenciesData[toCurrency].rub;
        return rubFrom / rubTo;
    };
    function getRate(fromCurrency, toCurrency) {
        if (convertRates[fromCurrency] && convertRates[fromCurrency][toCurrency]) {
            return convertRates[fromCurrency][toCurrency];
        }
        if (!convertRates[fromCurrency]) {
            convertRates[fromCurrency] = {};
        }
        convertRates[fromCurrency][toCurrency] = calculateRate(fromCurrency, toCurrency);
        return convertRates[fromCurrency][toCurrency];
    }
    function recalcAmount() {
        var fromCurrency = $fromSelect.value;
        var toCurrency = $toSelect.value;
        var rate = getRate(fromCurrency, toCurrency);
        var amount = parseFloat($amountInput.value || '0');
        var destValue = Math.round(rate * amount * 100) / 100;
        $resultValueContainer.innerHTML = 'precalculated result - ' + destValue;
    }
    var convertRates = {};
    $form.addEventListener('submit', function (ev) {
        ev.preventDefault();
        var fromCurrency = $fromSelect.value;
        var toCurrency = $toSelect.value;
        var amount = $amountInput.value;
        $resultValueContainer.innerHTML = 'Converting....';
        fetch([$form.getAttribute('action'), fromCurrency, toCurrency].join('/') + '?value=' + amount).then(function (responce) { return responce.json(); }).then(function (result) {
            if (!convertRates[fromCurrency]) {
                convertRates[fromCurrency] = {};
            }
            convertRates[fromCurrency][toCurrency] = Number(result.rate);
            $resultValueContainer.innerHTML = String(result.dest);
        });
    });
    $amountInput.addEventListener('keyup', recalcAmount);
    $fromSelect.addEventListener('change', recalcAmount);
    $toSelect.addEventListener('change', recalcAmount);
})();
