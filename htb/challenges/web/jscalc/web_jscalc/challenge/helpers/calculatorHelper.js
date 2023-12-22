module.exports = {
    calculate(formula) {
        try {
            console.log(eval(`(function() { return ${ formula } ;}())`))
            return eval(`(function() { return ${ formula } ;}())`);

        } catch (e) {
            if (e instanceof SyntaxError) {
                return e;
            }
        }
    }
}


// ocd