interface CurrencyType {
    code: string,
    name: string,
    symbol: string,
    rate_to_russian_rub: string
}

interface ResultType {
    from: CurrencyType
    to: CurrencyType
    rate: string
    src: number
    dest: number
}

interface CurrencyDataType {
    rub: number
    symbol: string
}

type CurrenciesDataType = Record<string, CurrencyDataType>
(function () {
    const $form = document.getElementById('converter-form');
    const $fromSelect = document.getElementById('currency-from') as HTMLSelectElement;
    const $toSelect = document.getElementById('currency-to') as HTMLSelectElement;
    const $amountInput = document.getElementById('amount') as HTMLInputElement;
    const $resultValueContainer = document.getElementById('result-container');
    const currenciesData: CurrenciesDataType = JSON.parse(document.getElementById('currencies-data').innerHTML);

    const calculateRate = (fromCurrency: string, toCurrency: string)=>{
        if (!currenciesData[fromCurrency] || !currenciesData[toCurrency]) {
            console.error("No data for some currency of ", fromCurrency, toCurrency);
            return
        }
        const rubFrom = currenciesData[fromCurrency].rub;
        const rubTo = currenciesData[toCurrency].rub;
        return rubFrom/rubTo;
    };

    function getRate(fromCurrency: string, toCurrency: string) {
        if (convertRates[fromCurrency] && convertRates[fromCurrency][toCurrency]) {
            return convertRates[fromCurrency][toCurrency];
        }
        if (!convertRates[fromCurrency]) {
            convertRates[fromCurrency] = {}
        }
        convertRates[fromCurrency][toCurrency] = calculateRate(fromCurrency, toCurrency);
        return convertRates[fromCurrency][toCurrency];
    }

    function recalcAmount() {
        const fromCurrency = $fromSelect.value;
        const toCurrency = $toSelect.value;
        const rate = getRate(fromCurrency, toCurrency);
        const amount = parseFloat($amountInput.value || '0');

        const destValue = Math.round(rate*amount * 100)/100;
        $resultValueContainer.innerHTML = 'precalculated result - ' + destValue;
    }

    const convertRates = {};
    $form.addEventListener('submit', (ev: Event) => {
        ev.preventDefault();
        const fromCurrency = $fromSelect.value;
        const toCurrency = $toSelect.value;
        const amount = $amountInput.value;
        $resultValueContainer.innerHTML = 'Converting....';
        fetch([$form.getAttribute('action'), fromCurrency, toCurrency].join('/') + '?value=' + amount).then(
            responce => responce.json()).then((result: ResultType) => {
            if (!convertRates[fromCurrency]) {
                convertRates[fromCurrency] = {}
            }
            convertRates[fromCurrency][toCurrency] = Number(result.rate);
            $resultValueContainer.innerHTML = String(result.dest)
        })
    });
    $amountInput.addEventListener('keyup', recalcAmount);
    $fromSelect.addEventListener('change', recalcAmount);
    $toSelect.addEventListener('change', recalcAmount);
})();