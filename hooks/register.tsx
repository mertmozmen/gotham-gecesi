import type { Register, ThemeSetArgs } from 'claude-code'

import { makeColors } from './make-colors.js'
import { SCENE } from './scene'

// Gotham gecesi, sarı-lacivert: gece laciverdi yüzeyler, sarı vurgu.
const { theme, problems } = makeColors({
  label: 'Gotham Gecesi (sarı-lacivert)',
  only: 'dark',
  roles: { accent: '#ffd400', danger: '#d0453c', success: '#4fa36a', warning: '#e8922a', pro: '#8f84d8' },
  dark: {
    gray: {
      anchors: {
        'surface-0': '#070c18',
        'surface-1': '#0c1324',
        'surface-2': '#111a2e',
        'surface-3': '#16203a',
        'text-primary': '#eceff6',
        'text-secondary': '#bcc4d6',
        'text-muted': '#8e98b0',
      },
    },
  },
})

const LOOK: ThemeSetArgs = {
  colors: theme,
  backdrop: { scene: 'gotham', glass: { blur: 6, tint: '#070c18', opacity: 0.55 } },
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    const unpainted = problems.find(line => line.startsWith("Desktop won't paint"))
    if (unpainted !== undefined) {
      $.ui.toast(unpainted)
    }
    const set = await $.theme.set(LOOK)
    if (!set.isDrawn) {
      $.ui.status(set.reason)
    }
    return next(e)
  })

  on('ui.render', { component: 'Backdrop' }, ($, e, next) => {
    if ((e.surface !== 'desktop' && e.surface !== 'mobile') || e.props.plugin !== 'gotham-gecesi') {
      return next(e)
    }
    const { Svg } = $.ui.resolve(e)
    return <Svg source={SCENE} alt="Yağmurlu gece şehri, bulutları tarayan projektör" isInteractive />
  })
}
