import { createI18n } from 'vue-i18n'
import type { I18n } from 'vue-i18n'
import en from '../locales/en'
import zh from '../locales/zh'

const i18n: I18n = createI18n({
  legacy: false,
  locale: localStorage.getItem('locale') || 'zh',
  fallbackLocale: 'zh',
  messages: {
    en,
    zh
  }
})

export default i18n 