import type { Register, ThemeSetArgs } from 'claude-code'

import { makeColors } from './make-colors.js'
import { SCENE } from './scene'

// Gotham gecesi: kurşuni siyah yüzeyler, sodyum lambası altını vurgu.
const { theme, problems } = makeColors({
  label: 'Gotham Gecesi',
  only: 'dark',
  roles: { accent: '#e6b422', danger: '#c8423a', success: '#6f9a5a', warning: '#d9922b', pro: '#8a7bb8' },
  dark: {
    gray: {
      anchors: {
        'surface-0': '#0b0d10',
        'surface-1': '#12151a',
        'surface-2': '#181c22',
        'surface-3': '#1e232a',
        'text-primary': '#e8e6df',
        'text-secondary': '#b9bcc0',
        'text-muted': '#8d939a',
      },
    },
  },
})

const LOOK: ThemeSetArgs = {
  colors: theme,
  backdrop: { scene: 'gotham', glass: { blur: 6, tint: '#0b0d10', opacity: 0.55 } },
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
