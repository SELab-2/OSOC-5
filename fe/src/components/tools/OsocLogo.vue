<template>
  <img v-if="$q.dark.isActive" style="max-width: min(80%, 550px); margin-left: max(10%, (100% - 550px)/2); filter: invert(0.25)"  src="https://osoc.be/img/logo/logo-osoc-color.svg" />
  <img v-else style="max-width: min(80%, 550px); margin-left: max(10%, (100% - 550px)/2)"  src="https://osoc.be/img/logo/logo-osoc-color.svg" />
</template>