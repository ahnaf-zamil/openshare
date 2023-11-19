<template>
  <q-layout>
    <div class="container-sm" style="max-width: 500px">
      <div>
        <h1
          class="text-h4 text-weight-light text-center q-mb-sm"
          color="secondary"
        >
          <span class="text-indigo-5">Open</span
          ><span class="text-blue-grey">Share</span>
        </h1>
        <p class="text-center text-weight-light">
          The freedom to share everything.
        </p>
      </div>
      <div class="column flex-center">
        <h5 class="text-h6 text-center q-my-md q-mt-lg">Create an account</h5>
        <q-input
          outlined
          class="full-width q-px-lg q-mb-md"
          v-model="name"
          label="Full Name"
        />
        <q-input
          outlined
          class="full-width q-px-lg q-mb-md"
          v-model="username"
          label="Username"
          hint="Your unique username across the platform"
          counter
          maxlength="20"
        />
        <q-input
          outlined
          class="full-width q-px-lg q-mb-md"
          v-model="email"
          type="email"
          label="Email"
        />
        <q-input
          outlined
          class="full-width q-px-lg q-mb-md"
          v-model="password"
          type="password"
          label="Password"
          minlength="8"
        />
        <q-btn
          unelevated
          rounded
          color="indigo-7"
          label="Register"
          size="md"
          class="q-mb-lg"
          padding="10px 60px"
        />
      </div>
      <q-separator inset />
      <div class="column flex-center">
        <h6 class="q-mt-lg text-weight-light text-center q-mb-md">
          Already have an account?
        </h6>
        <q-btn
          @click="this.$router.push('/login')"
          unelevated
          outline
          color="indigo-9"
          label="Log in"
          size="md"
          class="q-mb-xl"
          padding="10px 60px"
        />
      </div>
      <p class="copyright text-center text-grey-7">{{ copyright }}</p>
    </div>
  </q-layout>
</template>

<script lang="ts">
import { ref } from 'vue';
import { getCopyrightText } from '../util';

export default {
  setup() {
    return {
      name: ref(''),
      username: ref(''),
      password: ref(''),
      email: ref(''),
    };
  },
  data() {
    return {
      copyright: getCopyrightText(),
    };
  },
};
</script>
<style>
.copyright {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
}
</style>
