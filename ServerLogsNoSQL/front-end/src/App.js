import React from 'react';
import './App.css';

import {Switch, Route, withRouter } from 'react-router-dom';
import NavBar from './pages/navbar';

import Home from './pages/homepage';
import ApiMethods from './pages/api-methods/apiMethodsHome';

import Page401 from './pages/errors/error401/error401';
import Page404 from './pages/errors/error404/error404';

class App extends React.Component {

  render() {
      return (
          <div>
              <NavBar />

              <Switch>
                  <Route exact path="/"                   component={Home} />
                  <Route exact path="/welcome"            component={Home} />
                  <Route exact path="/home"               component={Home} />

                  <Route exact path="/api-methods"        component={ApiMethods} />
                  
                  {/* <Route exact path="/insert-log"         render={ () => isAuthenticated() ? <Insert />       : <Redirect to="/unauthorized" /> } /> */}

                  <Route exact path="/unauthorized"       component={Page401} />
                  <Route path="*" component={Page404} />
              </Switch>
          </div>
      );
  }
}

export default withRouter(App);