<template>
  <img v-if="$q.dark.isActive" style="max-width: min(80%, 550px); margin-left: max(10%, (100% - 550px)/2); filter: invert(0.25)"  src="https://osoc.be/img/logo/logo-osoc-color.svg" />
  <img v-else style="display: block; margin-left: auto; margin-right: auto; width: 60%; max-height: 250px"  src="https://osoc.be/img/logo/logo-osoc-color.svg" />
</template>