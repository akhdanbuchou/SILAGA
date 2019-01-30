<template>
    <div id="login-container" class="Login">
        <v-container>
            <v-layout row wrap align-center justify-center>
                <v-flex xs12 sm8 md4>
                    <v-card class="elevation-12 mt-5 mb-5">
                        <v-card-title>
                            <v-spacer></v-spacer>
                            <v-layout align-center justify-space-around wrap>
                                <v-flex xs2>
                                    <v-avatar align-center>
                                        <img
                                            src="../assets/silaga-logo.png"
                                            alt="silaga"
                                        >
                                    </v-avatar>
                                </v-flex>
                                <v-flex xs12 class="mt-3">
                                    <h6 class="font-weight-medium text-md-center">Login Sistem Laporan Gangguan (SILAGA)</h6>
                                </v-flex>
                            </v-layout>
                            <v-spacer></v-spacer>
                        </v-card-title>
                        <v-card-text>
                            <v-form>
                                <v-list-tile>
                                    <v-list-tile-action>
                                        <v-icon>mdi-account</v-icon>
                                    </v-list-tile-action>
                                    <v-text-field v-model="user.username" name="username" label="Username" type="text"></v-text-field>
                                </v-list-tile>
                                <v-list-tile>
                                    <v-list-tile-action>
                                        <v-icon>mdi-lock-open</v-icon>
                                    </v-list-tile-action>
                                    <v-text-field v-model="user.password" id="password" name="password" label="Password" type="password"></v-text-field>
                                </v-list-tile>
                                <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn color="green darken-1" @click="login()">Login</v-btn>
                                </v-card-actions>
                            </v-form>
                        </v-card-text>
                        
                    </v-card>
                    <v-layout>


                    </v-layout>
                </v-flex>
            </v-layout>
        </v-container>
    </div>
</template>

<script>
var defaultApi = 'http://127.0.0.1:5000/'
import axios from 'axios'
export default{
    name: 'Login',
    data() {
        return{
            user:{
                username: "",
                password:"",
            }
        }
    },
    methods:{
        login(){
            axios({
            method: 'post',
            url: defaultApi + 'validate',
            data:{
                username: this.user.username,
                password: this.user.password,
            }
            }).then(response => {
                this.$session.start()
                if(response){
                    this.$session.set('username', response.data.user.username)
                    axios.get(defaultApi + 'role?id=' + response.data.user.role)
                    .then(res => {
                        this.$session.set('currentUser', res.data)
                        this.$router.push({path: '/'})
                        
                    })
                }else{
                    console.log('gk masuk')
                }
            })
            
        }
    }
}

</script>

<style>
#login-container {
    /**background-image: url('../assets/login-page-01.png');
    min-height: 100%;
    background-size: cover;*/
}
</style>
