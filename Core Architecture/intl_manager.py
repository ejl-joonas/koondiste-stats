# i18n_manager.py
class I18nManager:
    """Manages internationalization and translations."""
    
    def __init__(self, config_manager):
        """Initialize with configuration manager."""
        self.config_manager = config_manager
        self.translations_path = "config/translations"
        self.current_language = self.config_manager.get("display.language", "en")
        self.translations = self._load_translations(self.current_language)
        self.taxonomies = self.config_manager.get("taxonomies", {})
        
    def _load_translations(self, language_code):
        """Load translations for specified language."""
        translations_file = os.path.join(self.translations_path, f"{language_code}.yaml")
        try:
            with open(translations_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Translations for {language_code} not found")
            return {}
            
    def set_language(self, language_code):
        """Change current language."""
        self.current_language = language_code
        self.translations = self._load_translations(language_code)
        self.config_manager.update_runtime("display.language", language_code)
        
    def get_text(self, key, default=None):
        """Get translated text for key."""
        value = self.translations.get(key)
        if value is None:
            return default if default else key
        return value
        
    def get_taxonomy_term(self, taxonomy, code):
        """Get translated taxonomy term."""
        if taxonomy in self.taxonomies and code in self.taxonomies[taxonomy]:
            term_data = self.taxonomies[taxonomy][code]
            return term_data.get(self.current_language, term_data.get('code', code))
        return code
        
    def translate_data_frame(self, df, column_mappings=None):
        """Translate a pandas DataFrame using column mappings."""
        if column_mappings is None:
            return df
            
        df_copy = df.copy()
        for col, mapping_info in column_mappings.items():
            if col in df_copy:
                taxonomy = mapping_info.get('taxonomy')
                if taxonomy:
                    df_copy[col + '_translated'] = df_copy[col].apply(
                        lambda x: self.get_taxonomy_term(taxonomy, x) if pd.notna(x) else ""
                    )
                    
        return df_copy