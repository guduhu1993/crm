"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
import requests
from rxconfig import config
import json
from datetime import datetime, timezone


API_URL = "http://localhost:8080"
API_LOGIN_URL = API_URL + "/token"
API_SIGNUP_URL = API_URL + "/register"


class TokenExp(rx.Base):
    access_token: str = ""
    exp: str = ""


class AccessToken(rx.State):  # 操作access_token
    LocalStorageState: str = rx.LocalStorage("{}", name="AccessToken")
    data: TokenExp = TokenExp
    is_login: bool = False

    def judge_token(self):
        data = TokenExp.parse_raw(self.LocalStorageState)
        if data.access_token and data.exp:
            if data.exp > datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S"):
                self.is_login = True
                return True

    def submit_login(self, form_data: dict):  # 登陆请求，获取access_token
        """Handle the form submit."""
        response_string = requests.post(API_LOGIN_URL, data=form_data).text
        if response_string:
            self.LocalStorageState = response_string
            self.judge_token()

    def token_is_valid(self):  # 验证token是否过期
        if not self.judge_token():
            return rx.redirect("/login")

    def token_is_valid_login(self):  # 验证token是否过期
        if self.judge_token():
            return rx.redirect("/home")
        
    def valid_token_2_home(self):  # 验证token跳转home
        if self.judge_token():
            return rx.redirect("/home")

    def set_login_state(self):
        self.is_login=False
        self.LocalStorageState='{}'
        rx.remove_local_storage("AccessToken")
        print(self.is_login)


class SignUp(rx.State):
    signup_success: bool
    username: str

    def submit_signup(self, form_data: dict):
        phone: str = form_data["phone"]
        self.form_data = form_data
        del self.form_data["phone"]
        response = requests.post(
            API_SIGNUP_URL + "?phone=" + phone, data=self.form_data
        )
        response_string = response.text
        if response_string:
            response_dict = json.loads(response_string)
            if "username" in response_dict and response.status_code == 200:
                self.username = response_dict["username"]
        print(self.username)


@rx.page(route="/login", title="登陆", on_load=AccessToken.token_is_valid_login)
def login():
    return rx.cond(
        AccessToken.is_login,
        rx.card(rx.center(
                rx.heading(
                    "已登录成功",
                    size="6",
                    as_="h2",
                    text_align="center",
                    width="100%",
                ),
                rx.button(
                        "进入主页",
                        type="submit",
                        size="3",
                        width="100%",
                        on_click=rx.redirect("/home")
                    ),
                direction="column",
                spacing="5",
                width="100%",
            ),
            size="4",
            max_width="28em",
            width="100%",), 
        rx.card(
            rx.center(
                rx.heading(
                    "登陆",
                    size="6",
                    as_="h2",
                    text_align="center",
                    width="100%",
                ),
                direction="column",
                spacing="5",
                width="100%",
            ),
            rx.form(
                rx.vstack(
                    rx.input(
                        placeholder="用户名",
                        name="username",
                        required=True,
                        min_length=6,
                        max_length=20,
                        size="3",
                        width="100%",
                    ),
                    rx.input(
                        placeholder="密码",
                        required=True,
                        name="password",
                        type="password",
                        min_length=6,
                        max_length=20,
                        size="3",
                        width="100%",
                    ),
                    rx.button(
                        "登陆",
                        type="submit",
                        size="3",
                        width="100%",
                    ),
                ),
                on_submit=AccessToken.submit_login,
                reset_on_submit=True,
            ),
            rx.center(
                rx.text("没有账号?", size="3"),
                rx.link("注册", href="/signup", size="3"),
                opacity="0.8",
                spacing="2",
                direction="row",
            ),
            size="4",
            max_width="28em",
            width="100%",
        ),
    )


@rx.page(route="/signup", title="注册")
def signup() -> rx.Component:
    return rx.cond(
        SignUp.username,
        login(),
        rx.center(
            rx.card(
                rx.center(
                    rx.heading(
                        "新建账号",
                        size="6",
                        as_="h2",
                        text_align="center",
                        width="100%",
                    ),
                    direction="column",
                    spacing="5",
                    width="100%",
                ),
                rx.form(
                    rx.input(
                        placeholder="用户名",
                        required=True,
                        name="username",
                        size="3",
                        width="100%",
                    ),
                    rx.input(
                        placeholder="手机号",
                        required=True,
                        name="phone",
                        min_length=11,
                        max_length=11,
                        size="3",
                        width="100%",
                    ),
                    rx.input(
                        placeholder="密码",
                        required=True,
                        name="password",
                        type="password",
                        min_length=6,
                        max_length=20,
                        size="3",
                        width="100%",
                    ),
                    rx.button(
                        "注册",
                        type="submit",
                        required=True,
                        size="3",
                        width="100%",
                        on_click=rx.redirect("/login"),
                    ),
                    on_submit=SignUp.submit_signup,
                    reset_on_submit=True,
                ),
                rx.center(
                    rx.text("已有账号?", size="3"),
                    rx.link("登陆", href="/login", size="3"),
                    opacity="0.8",
                    spacing="2",
                    direction="row",
                ),
                size="4",
                max_width="28em",
                width="100%",
            ),
        ),
    )


@rx.page(route="/home", title="主页", on_load=AccessToken.token_is_valid)
def home() -> rx.Component:
    return rx.button(
        " 登出 ",
        size="3",
        width="40%",
        on_click=AccessToken.set_login_state, #先点击修改is_login状态未false，
        on_blur=rx.remove_local_storage("AccessToken"),# 失焦删除token并刷新页面
    )


@rx.page(route="/redirect_page", title="跳转页", on_load=AccessToken.valid_token_2_home)
def redirect_page() -> rx.Component:
    return rx.text(
        " 跳转中 ",
    )


app = rx.App()
app.add_page(home)
app.add_page(login)
app.add_page(signup)
app.add_page(redirect_page)