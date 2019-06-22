import React from 'react';
import ReactDOM from 'react-dom';
import { shallow } from 'enzyme'
import UserForm from '../components/UserForm';


const formData = {
    username: '',
    email: '',
    password: ''
}
test('Registration Form renders without crashing', () => {
    const wrapper = shallow(<UserForm type='registration' title='Registration Form' formData={formData} />);
    const h1 = wrapper.find('h1');
    expect(h1.length).toBe(1);
    expect(h1.get(0).props.children).toBe('Registration Form');
    const formGroup = wrapper.find('.field').find('input');
    expect(formGroup.length).toBe(4);
    expect(formGroup.get(0).props.name).toBe('username');
    expect(formGroup.get(0).props.value).toBe('');
    expect(formGroup.get(0).props.type).toBe('text');
    expect(formGroup.get(1).props.name).toBe('email');
    expect(formGroup.get(1).props.value).toBe('');
    expect(formGroup.get(1).props.type).toBe('text');
    expect(formGroup.get(2).props.name).toBe('password');
    expect(formGroup.get(2).props.value).toBe('');
    expect(formGroup.get(2).props.type).toBe('password');
});


test('Login Form renders without crashing', () => {
    const wrapper = shallow(<UserForm type='login' title='Login Form' formData={formData} />);
    const h1 = wrapper.find('h1');
    expect(h1.length).toBe(1);
    expect(h1.get(0).props.children).toBe('Login Form');
    const formGroup = wrapper.find('.field').find('input');
    expect(formGroup.length).toBe(3);
    expect(formGroup.get(0).props.name).toBe('username');
    expect(formGroup.get(0).props.value).toBe('');
    expect(formGroup.get(0).props.type).toBe('text');
    expect(formGroup.get(1).props.name).toBe('password');
    expect(formGroup.get(1).props.value).toBe('');
    expect(formGroup.get(1).props.type).toBe('password');
});

test('Registration snapshot matches properly', () => {
    const tree = <UserForm type='registratoin' title='Registration Form' formData={formData} />
    expect(tree).toMatchSnapshot();
});

test('Login snapshot matches properly', () => {
    const tree = <UserForm type='login' title='Login Form' formData={formData} />
    expect(tree).toMatchSnapshot();
});