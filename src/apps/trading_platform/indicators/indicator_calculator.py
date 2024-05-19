import os
from typing import Dict, Any, List
from src.apps.trading_platform.indicators.indicators import Indicators
from src.apps.trading_platform.models import IndicatorSetting
from src.apps.trading_platform.indicators.indicator_enum import IndicatorEnum
from src.core import settings


class IndicatorsCalculator:
    def __init__(self, data: Any, indicators_instance: Any = Indicators) -> None:
        """
        Initialize the IndicatorsCalculator.

        Args:
            data: The market data to be used for calculation.
            indicators_instance: An instance of the Indicators class.
        """
        self.market_data = data
        self.indicator_calculator = indicators_instance()
        self.selected_indicators = self.get_selected_indicators()

    def get_selected_indicators(self) -> List[str]:
        """
        Retrieve the list of selected indicators from the database.

        Returns:
            List[str]: A list of selected indicator names.

        Raises:
            ValueError: If no indicators are found in the IndicatorSettings.
        """
        try:
            selected_indicators = list(
                IndicatorSetting.objects.values_list('indicator__name', flat=True)
            )
            return selected_indicators
        except IndicatorSetting.DoesNotExist as e:
            raise ValueError(
                f"Need set indicators. Not found indicators in IndicatorSettings: \n {e}"
            )

    def apply_set_indicators(self) -> Dict[str, Any]:
        """
        Apply the set indicators and calculate their values.

        Returns:
            Dict[str, Any]: A dictionary containing indicator names as keys and their calculated values as values.
        """
        combined_results: Dict[str, Any] = {}
        for indicator_name in self.selected_indicators:
            indicator_enum = IndicatorEnum(indicator_name)
            required_indicator_function = indicator_enum.get_required_indicator_function(
                indicator_name
            )
            required_indicator_name = required_indicator_function.__name__
            method_to_call = getattr(self.indicator_calculator, required_indicator_name)
            combined_results[indicator_name] = method_to_call(self.market_data)
            x = os.path.join(settings.BASE_DIR, 'indicators.csv')
        return combined_results

