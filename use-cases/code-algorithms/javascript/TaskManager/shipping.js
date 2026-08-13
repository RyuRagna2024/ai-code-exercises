/**
 * Interface / Base Strategy for Shipping Methods
 */
class ShippingStrategy {
  calculate(packageDetails, destinationCountry) {
    throw new Error("Method 'calculate()' must be implemented.");
  }
}

/**
 * Strategy: Standard Shipping
 */
class StandardShippingStrategy extends ShippingStrategy {
  calculate(packageDetails, destinationCountry) {
    const { weight, length, width, height } = packageDetails;
    const rates = { USA: 2.5, Canada: 3.5, Mexico: 4.0 };
    const rate = rates[destinationCountry] || 4.5; // Default international rate

    let cost = weight * rate;

    // Dimensional weight adjustment
    const volume = length * width * height;
    if (weight < 2 && volume > 1000) {
      cost += 5.0;
    }

    return cost.toFixed(2);
  }
}

/**
 * Strategy: Express Shipping
 */
class ExpressShippingStrategy extends ShippingStrategy {
  calculate(packageDetails, destinationCountry) {
    const { weight, length, width, height } = packageDetails;
    const rates = { USA: 4.5, Canada: 5.5, Mexico: 6.0 };
    const rate = rates[destinationCountry] || 7.5; // Default international rate

    let cost = weight * rate;

    // Large package surcharge
    const volume = length * width * height;
    if (volume > 5000) {
      cost += 15.0;
    }

    return cost.toFixed(2);
  }
}

/**
 * Strategy: Overnight Shipping
 */
class OvernightShippingStrategy extends ShippingStrategy {
  calculate(packageDetails, destinationCountry) {
    const { weight } = packageDetails;
    const rates = { USA: 9.5, Canada: 12.5 };

    if (!rates[destinationCountry]) {
      return "Overnight shipping not available for this destination";
    }

    const cost = weight * rates[destinationCountry];
    return cost.toFixed(2);
  }
}

/**
 * Context & Calculator
 */
class ShippingCalculator {
  constructor() {
    this.strategies = {
      standard: new StandardShippingStrategy(),
      express: new ExpressShippingStrategy(),
      overnight: new OvernightShippingStrategy()
    };
  }

  /**
   * Register a new strategy at runtime (Open/Closed Principle)
   */
  registerStrategy(methodName, strategyInstance) {
    this.strategies[methodName] = strategyInstance;
  }

  calculate(packageDetails, destinationCountry, shippingMethod) {
    const strategy = this.strategies[shippingMethod];
    if (!strategy) {
      throw new Error(`Unsupported shipping method: ${shippingMethod}`);
    }

    return strategy.calculate(packageDetails, destinationCountry);
  }
}

// Backward-compatible entry point wrapper
function calculateShippingCost(packageDetails, destinationCountry, shippingMethod) {
  const calculator = new ShippingCalculator();
  return calculator.calculate(packageDetails, destinationCountry, shippingMethod);
}

// ============================================================================
// UNIT TEST SUITE
// ============================================================================

function runShippingTests() {
  console.log("Running Strategy Pattern verification tests...\n");

  let allPassed = true;

  const assertEqual = (description, actual, expected) => {
    if (actual === expected) {
      console.log(`✅ PASSED: ${description}`);
    } else {
      console.error(`❌ FAILED: ${description} | Expected: "${expected}", Got: "${actual}"`);
      allPassed = false;
    }
  };

  const standardPackage = { weight: 5, length: 10, width: 10, height: 10 };
  const lightLargePackage = { weight: 1, length: 11, width: 10, height: 10 }; // Volume = 1100
  const hugePackage = { weight: 10, length: 20, width: 20, height: 15 };     // Volume = 6000

  // Standard Shipping Tests
  assertEqual("Standard USA", calculateShippingCost(standardPackage, 'USA', 'standard'), "12.50");
  assertEqual("Standard Canada", calculateShippingCost(standardPackage, 'Canada', 'standard'), "17.50");
  assertEqual("Standard Mexico", calculateShippingCost(standardPackage, 'Mexico', 'standard'), "20.00");
  assertEqual("Standard International (UK)", calculateShippingCost(standardPackage, 'UK', 'standard'), "22.50");
  assertEqual("Standard Surcharge (Vol > 1000 & W < 2)", calculateShippingCost(lightLargePackage, 'USA', 'standard'), "7.50");

  // Express Shipping Tests
  assertEqual("Express USA", calculateShippingCost(standardPackage, 'USA', 'express'), "22.50");
  assertEqual("Express Canada", calculateShippingCost(standardPackage, 'Canada', 'express'), "27.50");
  assertEqual("Express Mexico", calculateShippingCost(standardPackage, 'Mexico', 'express'), "30.00");
  assertEqual("Express International (Germany)", calculateShippingCost(standardPackage, 'Germany', 'express'), "37.50");
  assertEqual("Express Surcharge (Vol > 5000)", calculateShippingCost(hugePackage, 'USA', 'express'), "60.00");

  // Overnight Shipping Tests
  assertEqual("Overnight USA", calculateShippingCost(standardPackage, 'USA', 'overnight'), "47.50");
  assertEqual("Overnight Canada", calculateShippingCost(standardPackage, 'Canada', 'overnight'), "62.50");
  assertEqual("Overnight Unsupported Country", calculateShippingCost(standardPackage, 'Mexico', 'overnight'), "Overnight shipping not available for this destination");

  console.log(allPassed ? "\n🎉 All tests PASSED successfully!" : "\n❌ Some tests failed.");
}

// Execute tests when running node shipping.js
runShippingTests();